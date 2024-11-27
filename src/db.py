import sqlite3
import shutil
import os
from dataclasses import dataclass
from typing import Generator


# -------------------- Data Models --------------------
@dataclass
class Post:
    image: str
    text: str
    user: str


@dataclass
class User:
    username: str
    email: str
    hashed_password: str


# -------------------- Database Class --------------------
class Database:
    def __init__(self, db_name="posts.db"):
        """Initialize the database connection and ensure the tables exist."""
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        """Create the 'users' and 'posts' tables if they don't already exist."""
        with self.conn:
            # Create 'users' table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    hashed_password TEXT NOT NULL
                )
            ''')
            # Create 'posts' table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
                    image TEXT NOT NULL,
                    text TEXT NOT NULL,
                    user TEXT NOT NULL,
                    FOREIGN KEY (user) REFERENCES users(username)
                )
            ''')

    # -------------------- User Management --------------------
    def create_user(self, username: str, email: str, hashed_password: str):
        """Add a new user to the database."""
        try:
            with self.conn:
                self.conn.execute(
                    'INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)',
                    (username, email, hashed_password)
                )
        except sqlite3.IntegrityError as e:
            raise Exception(f"Username or email already exists: {e}")

    def get_user(self, username: str) -> User:
        """Retrieve a user from the database by username."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT username, email, hashed_password FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        if row:
            username, email, hashed_password = row
            return User(username=username, email=email, hashed_password=hashed_password)
        return None

    # -------------------- Post Management --------------------
    def save_image_to_folder(self, image_path: str, destination_folder: str = "images") -> str:
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

    def add_post(self, image_path: str, text: str, user: str):
        """Add a new post to the database, saving the image and storing its path."""
        saved_image_path = self.save_image_to_folder(image_path)
        with self.conn:
            self.conn.execute(
                'INSERT INTO posts (image, text, user) VALUES (?, ?, ?)',
                (saved_image_path, text, user)
            )

    def get_latest_post(self) -> Post:
        """Retrieve the most recently added post from the database."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT image, text, user FROM posts ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        if row:
            image, text, user = row
            return Post(image=image, text=text, user=user)
        return None

    # -------------------- Utility Methods --------------------
    def close(self):
        """Close the database connection."""
        self.conn.close()

    def wipe_database(self):
        """Delete all entries from the database."""
        with self.conn:
            self.conn.execute('DELETE FROM posts')
            self.conn.execute('DELETE FROM users')
        print("Database wiped clean.")


# -------------------- Dependency Injection --------------------
def get_db() -> Generator[Database, None, None]:
    """
    Provides a Database instance for dependency injection in FastAPI routes.
    """
    db = Database()
    try:
        yield db
    finally:
        db.close()


# ------------------- Tests save_image_to_folder --------------

def test_save_image_to_folder_valid():
    db = Database()
    test_image = "tests/test_image.jpg"  # Add a small dummy image in the `tests` folder
    os.makedirs("tests/images", exist_ok=True)
    
    saved_path = db.save_image_to_folder(test_image, "tests/images")
    assert os.path.exists(saved_path)

def test_save_image_to_folder_invalid():
    db = Database()
    with pytest.raises(Exception, match="Image file not found"):
        db.save_image_to_folder("non_existent_file.jpg")
