from fastapi import APIRouter, Depends, HTTPException, Form
from src.db import User, get_db, Database
from src.auth import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/register/")
async def register_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Database = Depends(get_db),
):
    """
    Register a new user.

    Parameters:
    - username: The desired username.
    - email: The user's email address.
    - password: The user's password.
    """
    try:
        hashed_password = hash_password(password)
        db.create_user(username, email, hashed_password)
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login/")
async def login_user(
    username: str = Form(...),
    password: str = Form(...),
    db: Database = Depends(get_db),
):
    """
    Log in a user and return a JWT token.

    Parameters:
    - username: The user's username.
    - password: The user's password.
    """
    user = db.get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/{username}/")
async def get_user_details(username: str, db: Database = Depends(get_db)):
    """
    Retrieve details of a specific user by username.

    Parameters:
    - username: The username of the user to retrieve.
    """
    user = db.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username, "email": user.email}
