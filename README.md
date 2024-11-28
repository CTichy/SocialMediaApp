```markdown
# SocialMediaApp

A simple social media app backend built using FastAPI.

## Features

- User authentication (registration and login).
- Secure password hashing and JWT-based access tokens.
- CRUD operations for user posts.
- Image upload with storage and resizing.
- API documentation using Swagger UI and ReDoc.
- SQLite database integration.

---

## Installation

### Prerequisites

- Python 3.10+ installed.
- `pip` for dependency management.

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SocialMediaApp.git
   ```

2. Navigate to the project directory:
   ```bash
   cd SocialMediaApp
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations (if necessary). For now, this app creates tables automatically on startup.

5. Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn src.api:app --reload
   ```

6. Open your browser to view the API documentation:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

### Authentication
- `POST /users/register/` - Register a new user.
- `POST /users/login/` - Authenticate a user and generate a token.

### User Management
- `GET /users/{username}/` - Get user details by username.

### Posts
- `POST /posts/` - Create a new post (image and text).
- `GET /posts/latest/` - Get the latest post.

---

## Running Tests

1. Install development dependencies (if not already installed):
   ```bash
   pip install pytest pytest-cov
   ```

2. Run tests with coverage:
   ```bash
   pytest --cov=src
   ```

3. View the coverage report:
   - Coverage HTML is generated in the `htmlcov` directory.

---

## Continuous Integration (CI)

This project uses GitHub Actions for CI. The `test.yml` workflow runs:
- Tests for all components using `pytest`.
- Coverage report generation with Codecov.

---

## Code Structure

```
SocialMediaApp/
├── src/
│   ├── api.py               # Main FastAPI application.
│   ├── auth.py              # Authentication logic (hashing, JWT creation/verification).
│   ├── db.py                # Database abstraction and utilities.
│   ├── utils/
│   │   ├── image.py         # Image validation and resizing utilities.
│   │   └── __init__.py      # Module initialization.
│   ├── routes/
│   │   ├── posts.py         # Post-related API endpoints.
│   │   ├── users.py         # User-related API endpoints.
│   │   └── __init__.py      # Module initialization.
├── tests/
│   ├── test_auth.py         # Tests for authentication logic.
│   ├── test_posts.py        # Tests for post-related endpoints.
│   ├── test_users.py        # Tests for user-related endpoints.
│   ├── test_utils.py        # Tests for utility functions (e.g., image handling).
├── requirements.txt         # Python dependencies.
├── test.yml                 # GitHub Actions CI configuration.
└── README.md                # Project documentation.
```

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes with descriptive messages.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

For questions or issues, please contact:
- **Name**: Carlos E. Tichy
- **Email**: carlos.tichy@gmail.com
```
