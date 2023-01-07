import tensorflow as tf
from PIL import Image


DEFAULT_IMAGE_SIZE = 256


def generate_train_val_ds(path: str, image_size: tuple, batch_size: int, val_split=0.2):
    train_ds = tf.keras.utils.image_dataset_from_directory(
        path,
        validation_split=val_split,
        subset="training",
        seed=123,
        image_size=image_size,
        batch_size=batch_size)

    val_ds = tf.keras.utils.image_dataset_from_directory(
        path,
        validation_split=val_split,
        subset="validation",
        seed=123,
        image_size=image_size,
        batch_size=batch_size)

    return train_ds, val_ds


def get_batch_size(dataset_elements_num):
    pass


def get_image_size(img: Image) -> int:
    width, height = img.size
    if width < DEFAULT_IMAGE_SIZE or height < DEFAULT_IMAGE_SIZE:
        return min(width, height)
    return DEFAULT_IMAGE_SIZE


def get_dropout_num():
    pass


def get_epochs_num():
    pass


def get_neurones_num():
    pass


def rescale_image_pixels(image):
    return image

