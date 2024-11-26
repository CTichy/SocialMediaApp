from PIL import Image
import os

def validate_image_format(image_path: str):
    """
    Validate that the image is in a supported format.
    """
    valid_formats = ["JPEG", "PNG"]
    try:
        with Image.open(image_path) as img:
            if img.format not in valid_formats:
                raise ValueError(f"Unsupported image format: {img.format}")
    except Exception as e:
        raise ValueError(f"Invalid image file: {e}")

def resize_image(image_path: str, size=(500, 500)):
    """
    Resize the image to the specified dimensions.
    """
    try:
        with Image.open(image_path) as img:
            img = img.resize(size)
            img.save(image_path)
    except Exception as e:
        raise ValueError(f"Failed to resize image: {e}")
