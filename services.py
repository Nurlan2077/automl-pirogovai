from PIL import Image

DEFAULT_SIZE = 256

def get_image_size(img: Image) -> int:
    width, height = img.size
    if width < DEFAULT_SIZE or height < DEFAULT_SIZE:
        return min(width, height)
    return DEFAULT_SIZE