import sqlite3
import shutil
import os
from dataclasses import dataclass

@dataclass
class Post:
    image: str  # Path to the image file
    text: str   # Comment or description of the post
    user: str   # Username of the person creating the post


class PostDatabase:
    def __init__(self, db_name="posts.db"):
        """Initialize the database connection and ensure the table exists."""
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        """Create the 'posts' table if it doesn't already exist."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
                    image TEXT NOT NULL,
                    text TEXT NOT NULL,
                    user TEXT NOT NULL
                )
            ''')

    def save_image_to_folder(self, image_path, destination_folder="images"):
        """
        Save the image to the destination folder and return the relative path to the saved image.
        """
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)  # Create the folder if it doesn't exist

        filename = os.path.basename(image_path)
        destination_path = os.path.join(destination_folder, filename)

        try:
            shutil.copy2(image_path, destination_path)
            # Debug: Check sizes
            source_size = os.path.getsize(image_path)
            dest_size = os.path.getsize(destination_path)
            print(f"Source size: {source_size} bytes, Destination size: {dest_size} bytes")
        except FileNotFoundError:
            raise Exception(f"Image file not found: {image_path}")
        except IOError as e:
            raise Exception(f"Failed to copy image file: {e}")

        return destination_path

    def add_post(self, image_path, text, user):
        """Add a new post to the database, saving the image and storing its path."""
        saved_image_path = self.save_image_to_folder(image_path)
        with self.conn:
            self.conn.execute(
                'INSERT INTO posts (image, text, user) VALUES (?, ?, ?)',
                (saved_image_path, text, user)
            )

    def get_latest_post(self):
        """Retrieve the most recently added post from the database."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT image, text, user FROM posts ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        if row:
            image, text, user = row
            return Post(image=image, text=text, user=user)
        return None


if __name__ == "__main__":
    db = PostDatabase()

    # Example usage
    example_image_path = "C:\\Users\\Carlos Tichy\\Pictures\\pig.jpeg"
    db.add_post(image_path=example_image_path, text="My third post!", user="user123")

    latest_post = db.get_latest_post()
    if latest_post:
        print(f"Latest post:\n  Image Path: {latest_post.image}\n  Text: {latest_post.text}\n  User: {latest_post.user}")
    else:
        print("No posts found.")
