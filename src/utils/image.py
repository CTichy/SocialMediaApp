from PIL import Image
import os


def validate_image_format(image_path: str) -> bool:
    """
    Validate that the image is in a supported format.

    Parameters:
    - image_path: Path to the image file.

    Returns:
    - True if the image format is valid.

    Raises:
    - ValueError if the image format is invalid or cannot be opened.
    """
    valid_formats = ["JPEG", "PNG"]
    try:
        with Image.open(image_path) as img:
            if img.format not in valid_formats:
                raise ValueError(f"Unsupported image format: {img.format}")
        return True
    except Exception as e:
        raise ValueError(f"Invalid image file: {e}")


def resize_image(image_path: str, output_size=(500, 500)) -> str:
    """
    Resize the image to the specified dimensions.

    Parameters:
    - image_path: Path to the image file.
    - output_size: Tuple containing the width and height of the resized image.

    Returns:
    - Path to the resized image.

    Raises:
    - ValueError if resizing fails.
    """
    try:
        with Image.open(image_path) as img:
            resized_img = img.resize(output_size)
            resized_path = f"{os.path.splitext(image_path)[0]}_resized{os.path.splitext(image_path)[1]}"
            resized_img.save(resized_path)
        return resized_path
    except Exception as e:
        raise ValueError(f"Failed to resize image: {e}")
