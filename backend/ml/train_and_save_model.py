import sys
import os
import tensorflow as tf
from keras import layers
from PIL import Image
from keras.models import Sequential
from loss_funcs import LOSS_FUNCS_REVERSED
from optimizers import OPTIMIZERS_REVERSED

DEFAULT_IMAGE_SIZE = 256
DEFAULT_BATCH_SIZE = 32
DEFAULT_DROPOUT = 0.2
DEFAULT_EPOCHS = 1


def generate_train_val_ds(dataset_path: str, image_size: tuple[int, int], val_split=0.2):
    batch_size = get_batch_size()

    train_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_path,
        validation_split=val_split,
        subset="training",
        seed=123,
        image_size=image_size,
        batch_size=batch_size)

    val_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_path,
        validation_split=val_split,
        subset="validation",
        seed=123,
        image_size=image_size,
        batch_size=batch_size)

    class_names = train_ds.class_names
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    return train_ds, val_ds, class_names


def get_image_size(dataset_path: str) -> tuple[int, int]:
    img = get_first_image(dataset_path)
    width, height = img.size
    if width < DEFAULT_IMAGE_SIZE or height < DEFAULT_IMAGE_SIZE:
        width = height = min(width, height)
        return (width, height)
    return (DEFAULT_IMAGE_SIZE, DEFAULT_IMAGE_SIZE)


def get_first_image(dataset_path: str) -> Image:
    first_class_name = os.listdir(dataset_path)[0]
    first_image_name = os.listdir(dataset_path + first_class_name)[0]
    return Image.open(dataset_path + first_class_name + "/" + first_image_name)


def get_batch_size(dataset_size: int = 0) -> int:
    # batch size = available GPU memory bytes / 4 / (size of tensors + trainable parameters)
    return DEFAULT_BATCH_SIZE


def get_dropout_num():
    return DEFAULT_DROPOUT


optimizer_name = sys.argv[1]
optimizer = OPTIMIZERS_REVERSED[optimizer_name]

loss_func_name = sys.argv[2]
loss_func = LOSS_FUNCS_REVERSED[loss_func_name]

epochs = int(sys.argv[3])
dataset_path = sys.argv[4]
models_path = sys.argv[5]

width, height = get_image_size(dataset_path)
train_ds, val_ds, class_names = generate_train_val_ds(dataset_path, (width, height))

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal", input_shape=(width, height, 3)),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

dropout = get_dropout_num()
num_classes = len(class_names)
sequential_layers = [
    data_augmentation,
    layers.Rescaling(1. / 255),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(dropout),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes, name="outputs")
]

model = Sequential(sequential_layers)
model.compile(optimizer=optimizer, loss=loss_func, metrics=['accuracy'])
history = model.fit(train_ds, validation_data=val_ds, epochs=epochs)

model._name = optimizer_name + "_" + loss_func.name
model.save(models_path + optimizer_name + "_" + loss_func.name + ".h5")
del model
