import unittest
import os
from app import Post, PostDatabase

class TestPostDatabase(unittest.TestCase):
    def setUp(self):
        """
        Create a new in-memory database for each test.
        This avoids the need for a physical file and ensures clean tests.
        """
        self.db = PostDatabase(":memory:")  # Use in-memory database for isolated testing

    def tearDown(self):
        """
        Clean up after each test by closing the database connection.
        """
        self.db.conn.close()

    def test_add_post(self):
        """
        Test adding a post to the database and retrieving it.
        """
        # Add a new post
        self.db.add_post(image_path="images//chicken.jpeg", text="Test post", user="user1")

        # Retrieve the latest post
        latest_post = self.db.get_latest_post()

        # Assert that the post was added and data matches
        self.assertIsNotNone(latest_post)
        self.assertEqual(latest_post.image, "chicken.jpeg")
        self.assertEqual(latest_post.text, "Test post")
        self.assertEqual(latest_post.user, "user1")

    def test_get_latest_post_empty(self):
        """
        Test retrieving a post from an empty database.
        Should return None.
        """
        latest_post = self.db.get_latest_post()
        self.assertIsNone(latest_post)

    def test_multiple_posts(self):
        """
        Test adding multiple posts and retrieving the latest one.
        """
        # Add multiple posts
        self.db.add_post(image_path="images//donkey.jpeg", text="Post 1", user="user1")
        self.db.add_post(image_path="images//pig.jpeg", text="Post 2", user="user2")

        # Retrieve the latest post
        latest_post = self.db.get_latest_post()

        # Assert that the latest post matches the last one added
        self.assertIsNotNone(latest_post)
        self.assertEqual(latest_post.image, "pig.jpeg")
        self.assertEqual(latest_post.text, "Post 2")
        self.assertEqual(latest_post.user, "user2")

    def test_wipe_database(self):
        """
        Test wiping the database by deleting all entries.
        """
        # Add a post
        self.db.add_post(image_path="images//chicken.jpeg", text="To be deleted", user="user1")

        # Wipe the database (simulate by clearing the table)
        with self.db.conn:
            self.db.conn.execute("DELETE FROM posts")

        # Check that the database is empty
        latest_post = self.db.get_latest_post()
        self.assertIsNone(latest_post)


if __name__ == "__main__":
    unittest.main()
