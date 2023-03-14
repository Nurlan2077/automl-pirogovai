import asyncio
import glob
import logging
import os
from typing import Optional

import numpy as np
import tensorflow as tf
from PIL import Image
from sklearn.metrics import classification_report

from loss_funcs import LOSS_FUNCS_REVERSED
from optimizers import OPTIMIZERS_REVERSED
from fastapi import WebSocket
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

DEFAULT_IMAGE_SIZE = 256
DEFAULT_BATCH_SIZE = 32
DEFAULT_DROPOUT = 0.2
DEFAULT_EPOCHS = 10


async def learn_models(websocket: WebSocket, dataset_path: str, models_path: str, markup_path: Optional[str],
                       params: dict[str, str | int]) -> tuple[str, dict, int]:
    tf.config.optimizer.set_experimental_options({'layout_optimizer': False})
    width, height = get_image_size(dataset_path)
    _, val_ds, class_names = generate_train_val_ds(dataset_path, (width, height))
    epochs = params["epochs"]
    total_count = len(params["optimizer"]) * len(params["lossFunction"])
    logging.info(f"Total count: {total_count}")
    i = 0

    for optimizer in OPTIMIZERS_REVERSED:
        if optimizer not in params["optimizer"]:
            continue
        for loss_func in LOSS_FUNCS_REVERSED:
            if loss_func not in params["lossFunction"]:
                continue
            os.system("python ml/train_and_save_model.py {} {} {} {} {}".
                      format(optimizer, loss_func, epochs, dataset_path, models_path))
            i += 1
            logging.info(f"{i * 100 / total_count}%")
            await websocket.send_text(f"{i * 100 / total_count}%")
            await asyncio.sleep(1)
            tf.keras.backend.clear_session()

    path_to_model, report = get_best_model_and_metrics(models_path, val_ds, class_names)
    metrics = {
        "accuracy": report["accuracy"],
        "precision": report["weighted avg"]["precision"],
        "recall": report["weighted avg"]["recall"],
        "f1-score": report["weighted avg"]["f1-score"]
    }

    logging.info(f"model path: {path_to_model}")
    logging.info(f"metrics: {metrics}")

    return path_to_model, metrics, epochs


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


def get_best_model_and_metrics(models_path, val_ds, class_names: list[str]):
    prev = 0
    best_model_file = None
    report = None

    val_labels = np.concatenate([y for x, y in val_ds], axis=0)

    for file in glob.glob(models_path + "*.h5"):
        model = tf.keras.models.load_model(file)
        preds = tf.nn.softmax(model.predict(val_ds))
        y_pred = np.argmax(preds, axis=1)
        report = classification_report(val_labels, y_pred, target_names=class_names, output_dict=True)

        if report["weighted avg"]["f1-score"] > prev:
            prev = report["weighted avg"]["f1-score"]
            best_model_file = file

    return best_model_file, report


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


def save_model(model, dataset_path: str) -> str:
    path = dataset_path + model.name + ".h5"
    model.save(path)
    return path


def get_batch_size(dataset_size: int = 0) -> int:
    # batch size = available GPU memory bytes / 4 / (size of tensors + trainable parameters)
    return DEFAULT_BATCH_SIZE


def get_dropout_num():
    return DEFAULT_DROPOUT


def get_epochs_num():
    return DEFAULT_EPOCHS
