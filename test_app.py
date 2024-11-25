import unittest
from app import Post, PostDatabase

class TestPostDatabase(unittest.TestCase):
    def setUp(self):
        self.db = PostDatabase(":memory:")  # Use an in-memory database

    def test_add_post(self):
        post = Post("image.jpg", "Test post", "user1")
        self.db.add_post(post)
        latest_post = self.db.get_latest_post()
        self.assertEqual(latest_post.image, "image.jpg")
        self.assertEqual(latest_post.text, "Test post")
        self.assertEqual(latest_post.user, "user1")

    def test_get_latest_post_empty(self):
        latest_post = self.db.get_latest_post()
        self.assertIsNone(latest_post)

if __name__ == "__main__":
    unittest.main()
