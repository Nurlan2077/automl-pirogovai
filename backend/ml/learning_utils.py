import os
import numpy as np
import tensorflow as tf
from PIL import Image
from keras import layers
from keras.models import Sequential
from sklearn.metrics import classification_report
from loss_funcs import LOSS_FUNCS
from optimizers import OPTIMIZERS


DEFAULT_IMAGE_SIZE = 256
DEFAULT_BATCH_SIZE = 32
DEFAULT_DROPOUT = 0.2
DEFAULT_EPOCHS = 10


def learn_models(dataset_path: str, markup_path: str, params: dict | None = None) -> tuple[str, dict]:
    width, height = __get_image_size(dataset_path)
    train_ds, val_ds, class_names = __generate_train_val_ds(dataset_path, (width, height))

    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal", input_shape=(width, height, 3)),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
    ])

    dropout = __get_dropout_num()
    num_classes = len(class_names)
    sequential_layers = [
        data_augmentation,
        layers.Rescaling(1./255),
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

    models = []
    epochs = __get_epochs_num()

    for optimizer in OPTIMIZERS:
        for loss_func in LOSS_FUNCS:

            optimizer_name = str(optimizer).split(".")[-1].split(" ")[0]
            model = Sequential(sequential_layers)
            model.compile(optimizer=optimizer, loss=loss_func, metrics=['accuracy'])
            model.fit(train_ds, validation_data=val_ds, epochs=epochs)
            model._name = optimizer_name + "_" + loss_func.name
            models.append(model)
            
            del model
            tf.keras.backend.clear_session()

    model, metrics = __get_best_model_and_metrics(models, val_ds, class_names)
    path_to_model = __save_model(model, dataset_path)
    return path_to_model, metrics


def __generate_train_val_ds(dataset_path: str, image_size: tuple[int, int], val_split=0.2):
    batch_size = __get_batch_size()
    
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


def __get_best_model_and_metrics(models, val_ds, class_names: list[str]):
    prev = 0
    best_model = None
    
    val_labels = np.concatenate([y for x, y in val_ds], axis=0)

    for model in models:
        preds = tf.nn.softmax(model.predict(val_ds))
        y_pred = np.argmax(preds, axis=1)
        report = classification_report(val_labels, y_pred, target_names=class_names, output_dict=True)
                
        if report["weighted avg"]["f1-score"] > prev:
            prev = report["weighted avg"]["f1-score"]
            best_model = model
            
    return best_model, report


def __get_image_size(dataset_path: str) -> tuple[int, int]:
    img = __get_first_image(dataset_path)
    width, height = img.size
    if width < DEFAULT_IMAGE_SIZE or height < DEFAULT_IMAGE_SIZE:
        width = height = min(width, height)
        return (width, height)
    return (DEFAULT_IMAGE_SIZE, DEFAULT_IMAGE_SIZE)


def __get_first_image(dataset_path: str) -> Image:
    first_class_name = os.listdir(dataset_path)[0]
    first_image_name = os.listdir(dataset_path + first_class_name)[0]
    return Image.open(dataset_path + first_class_name + "/" + first_image_name)


def __save_model(model, dataset_path: str) -> str:
    path = dataset_path + model.name + ".h5"
    model.save(path)
    return path


def __get_batch_size(dataset_size: int = 0) -> int:
    # batch size = available GPU memory bytes / 4 / (size of tensors + trainable parameters)
    return DEFAULT_BATCH_SIZE


def __get_dropout_num():
    return DEFAULT_DROPOUT


def __get_epochs_num():
    return DEFAULT_EPOCHS