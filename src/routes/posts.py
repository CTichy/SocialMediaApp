from fastapi import APIRouter, HTTPException, UploadFile, Form
from src.db import Database

router = APIRouter()
db = Database()  # Instantiate the new Database class

@router.post("/")
async def create_post(
    image: UploadFile, 
    text: str = Form(...), 
    user: str = Form(...)
):
    """
    API endpoint to create a new post.

    Parameters:
    - image: Image file to upload.
    - text: Description of the post.
    - user: Username of the post creator.
    """
    try:
        # Save the image temporarily
        temp_image_path = f"temp_{image.filename}"
        with open(temp_image_path, "wb") as temp_file:
            temp_file.write(await image.read())

        # Add the post to the database
        db.add_post(image_path=temp_image_path, text=text, user=user)

        # Clean up temporary file
        os.remove(temp_image_path)

        return {"message": "Post created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/latest/")
async def get_latest_post():
    """
    API endpoint to get the most recently created post.
    """
    latest_post = db.get_latest_post()
    if not latest_post:
        raise HTTPException(status_code=404, detail="No posts found")

    return {
        "image": latest_post.image,
        "text": latest_post.text,
        "user": latest_post.user,
    }
