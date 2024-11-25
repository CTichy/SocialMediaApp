import unittest
import os
import shutil
from app import Post, PostDatabase


class TestPostDatabase(unittest.TestCase):
    def setUp(self):
        # Use an in-memory database for isolated testing
        self.db = PostDatabase(":memory:")

        # Create a temporary images folder for testing
        self.test_images_folder = "test_images"
        if not os.path.exists(self.test_images_folder):
            os.makedirs(self.test_images_folder)

        # Create a dummy image file for testing
        self.dummy_image_path = os.path.join(self.test_images_folder, "dummy_image.jpg")
        with open(self.dummy_image_path, "wb") as f:
            f.write(b"This is a dummy image content.")

    def tearDown(self):
        # Clean up the temporary images folder
        if os.path.exists(self.test_images_folder):
            shutil.rmtree(self.test_images_folder)

    def test_add_post(self):
        # Add a post with a dummy image
        self.db.add_post(image_path=self.dummy_image_path, text="Test post", user="user1")

        # Check that the image is copied to the images folder
        saved_image_path = os.path.join("images", "dummy_image.jpg")
        self.assertTrue(os.path.exists(saved_image_path))

        # Check that the post details are stored correctly in the database
        latest_post = self.db.get_latest_post()
        self.assertIsNotNone(latest_post)
        self.assertEqual(latest_post.image, saved_image_path)
        self.assertEqual(latest_post.text, "Test post")
        self.assertEqual(latest_post.user, "user1")

    def test_get_latest_post_empty(self):
        # Test retrieving from an empty database
        latest_post = self.db.get_latest_post()
        self.assertIsNone(latest_post)


if __name__ == "__main__":
    unittest.main()
