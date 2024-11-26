from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext

# Secret key and algorithm for JWT
SECRET_KEY = "your_secret_key"  # Replace with a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------- Password Utilities --------------------
def hash_password(password: str) -> str:
    """
    Hash a plain-text password.

    Parameters:
    - password: Plain-text password.

    Returns:
    - Hashed password as a string.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a hashed password.

    Parameters:
    - plain_password: The password provided by the user.
    - hashed_password: The stored hashed password.

    Returns:
    - True if the password matches, otherwise False.
    """
    return pwd_context.verify(plain_password, hashed_password)


# -------------------- Token Utilities --------------------
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token.

    Parameters:
    - data: Dictionary containing the data to encode in the token.
    - expires_delta: Expiration time delta for the token.

    Returns:
    - Encoded JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT token.

    Parameters:
    - token: The JWT token to decode.

    Returns:
    - Decoded data as a dictionary.

    Raises:
    - JWTError if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise Exception(f"Invalid token: {e}")
