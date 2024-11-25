import sqlite3
from dataclasses import dataclass

@dataclass
class Post:
    image: str
    text: str
    user: str

class PostDatabase:
    def __init__(self, db_name="posts.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
                    image TEXT NOT NULL,
                    text TEXT NOT NULL,
                    user TEXT NOT NULL
                )
            ''')

    def add_post(self, post: Post):
        with self.conn:
            self.conn.execute(
                'INSERT INTO posts (image, text, user) VALUES (?, ?, ?)',
                (post.image, post.text, post.user)
            )

    def get_latest_post(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT image, text, user FROM posts ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        if row:
            return Post(*row)
        return None

if __name__ == "__main__":
    db = PostDatabase()
    new_post = Post(image="image.jpg", text="Hello World!", user="user123")
    db.add_post(new_post)
    print("Latest post:", db.get_latest_post())
