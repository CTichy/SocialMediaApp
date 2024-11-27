import pytest
from src.utils.image import validate_image_format, resize_image
from PIL import Image
import tempfile
import os

def test_validate_image_format_valid():
    # Create a temporary valid image
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image:
        img = Image.new("RGB", (100, 100), color="blue")
        img.save(temp_image.name, format="JPEG")
        temp_image.close()

        # Test the valid image
        assert validate_image_format(temp_image.name) is True

        # Cleanup
        os.remove(temp_image.name)

def test_validate_image_format_invalid():
    # Create a temporary invalid file
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
        temp_file.write(b"This is not an image")
        temp_file.close()

        # Test the invalid file
        with pytest.raises(ValueError, match="Invalid image file"):
            validate_image_format(temp_file.name)

        # Cleanup
        os.remove(temp_file.name)

def test_resize_image():
    # Create a temporary valid image
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image:
        img = Image.new("RGB", (500, 500), color="blue")
        img.save(temp_image.name, format="JPEG")
        temp_image.close()

        # Resize the image
        resized_image_path = resize_image(temp_image.name, (100, 100))

        # Verify the new size
        with Image.open(resized_image_path) as resized_img:
            assert resized_img.size == (100, 100)

        # Cleanup
        os.remove(temp_image.name)
        os.remove(resized_image_path)
