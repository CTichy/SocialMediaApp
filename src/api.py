from fastapi import FastAPI
from src.routes.posts import router as posts_router
from src.routes.users import router as users_router

# Initialize FastAPI
app = FastAPI(
    title="Social Media App",
    description="A backend for managing users and posts in a social media app.",
    version="1.0.0",
    contact={
        "name": "Carlos E. Tichy",
        "email": "carlos.tichy@gmail.com",
    },
)

# Include routes
app.include_router(posts_router, prefix="/posts", tags=["Posts"])
app.include_router(users_router, prefix="/users", tags=["Users"])
