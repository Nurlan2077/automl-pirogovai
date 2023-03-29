import asyncio
import glob
import logging
import os
import shutil
import numpy as np
import tensorflow as tf
from typing import Optional
from itertools import product
from PIL import Image
from sklearn.metrics import classification_report
from fastapi import WebSocket
from tensorflow.compat.v1 import ConfigProto, InteractiveSession
from keras import layers
from keras.models import Sequential
from keras.callbacks import EarlyStopping, ModelCheckpoint, TerminateOnNaN

from loss_funcs import LOSS_FUNCS_REVERSED
from optimizers import OPTIMIZERS_REVERSED

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

tf.get_logger().setLevel(logging.ERROR)
logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

DEFAULT_IMG_SIZE = 256
DEFAULT_BATCH_SIZE = 32
DEFAULT_DROPOUT = 0.2
DEFAULT_EPOCHS = 10


async def learn_models(websocket: WebSocket, dataset_path: str, 
                       models_path: str, markup_path: Optional[str],
                       params: dict[str, str | int]) -> tuple[str, dict, int]:
    
    img_size = get_image_size(dataset_path)
    train, val, classes = generate_train_val_ds(dataset_path, img_size)

    learned = 0
    epochs = params["epochs"]
    total_count = len(params["optimizer"]) * len(params["lossFunction"])
    logging.info(f"Total count: {total_count}")

    await websocket.send_text("1%")
    await asyncio.sleep(1)
    for optimizer, loss in product(params['optimizer'], params['lossFunction']):
        train_model(optimizer, loss, epochs, models_path, train, val, img_size, classes)
        learned += 1
        logging.info(f"{learned * 100 / total_count}%")
        await websocket.send_text(f"{learned * 100 / total_count}%")
        await asyncio.sleep(1)

    model_path, report = get_best_model_and_metrics(models_path, val, classes)
    metrics = {
        "accuracy": report["accuracy"],
        "precision": report["weighted avg"]["precision"],
        "recall": report["weighted avg"]["recall"],
        "f1-score": report["weighted avg"]["f1-score"]
    }
    logging.info(f"model path: {model_path}")
    logging.info(f"metrics: {metrics}")

    return model_path, metrics, epochs


def generate_train_val_ds(dataset_path: str, image_size: tuple[int, int], val_split=0.2):
    train = tf.keras.utils.image_dataset_from_directory(
        dataset_path,
        validation_split=val_split,
        subset="training",
        seed=123,
        image_size=image_size,
        batch_size=DEFAULT_BATCH_SIZE)

    val = tf.keras.utils.image_dataset_from_directory(
        dataset_path,
        validation_split=val_split,
        subset="validation",
        seed=123,
        image_size=image_size,
        batch_size=DEFAULT_BATCH_SIZE)

    classes = train.class_names
    AUTOTUNE = tf.data.AUTOTUNE
    train = train.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val = val.cache().prefetch(buffer_size=AUTOTUNE)
    return train, val, classes


def train_model(optimizer_name, loss_name, epochs, models_path, train, val, img_size, classes):
    optimizer = OPTIMIZERS_REVERSED[optimizer_name]
    loss = LOSS_FUNCS_REVERSED[loss_name]

    width, height = img_size
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal", input_shape=(width, height, 3)),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
    ])

    sequential_layers = [
        data_augmentation,
        layers.Rescaling(1. / 255),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(DEFAULT_DROPOUT),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(len(classes), name="outputs")
    ]

    model_name = optimizer_name + "_" + loss_name
    model_path = models_path + model_name + ".tf"
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=5),
        ModelCheckpoint(filepath=model_path, save_best_only=True),
        TerminateOnNaN()
    ]

    model = Sequential(sequential_layers)
    model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])
    model.fit(train, validation_data=val, epochs=epochs, callbacks=callbacks)

    if os.path.exists(model_path):
        tf_model = tf.keras.models.load_model(model_path)
        tf_model.save(model_path[:-2] + "h5")
        shutil.rmtree(model_path)
        
    tf.keras.backend.clear_session()


def get_best_model_and_metrics(models_path, val, class_names: list[str]):
    prev = 0
    best_model_file = None
    report = None
    best_report = None

    val_labels = np.concatenate([y for _, y in val], axis=0)

    for file in glob.glob(models_path + "*.h5"):
        model = tf.keras.models.load_model(file)
        preds = tf.nn.softmax(model.predict(val))
        y_pred = np.argmax(preds, axis=1)
        report = classification_report(val_labels, y_pred, target_names=class_names, output_dict=True)

        if report["weighted avg"]["f1-score"] > prev:
            prev = report["weighted avg"]["f1-score"]
            best_report = report
            best_model_file = file

    return best_model_file, best_report


def get_image_size(dataset_path: str) -> tuple[int, int]:
    img = get_first_image(dataset_path)
    width, height = img.size
    if width < DEFAULT_IMG_SIZE or height < DEFAULT_IMG_SIZE:
        width = height = min(width, height)
        return (width, height)
    return (DEFAULT_IMG_SIZE, DEFAULT_IMG_SIZE)


def get_first_image(dataset_path: str) -> Image:
    first_class_name = os.listdir(dataset_path)[0]
    first_image_name = os.listdir(dataset_path + first_class_name)[0]
    return Image.open(dataset_path + first_class_name + "/" + first_image_name)
