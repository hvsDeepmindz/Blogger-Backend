from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status, Request
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.blogModel import TbITBlog
from models.blogMediaModel import TbITMedia
from schemas.blogMediaSchemas import (
    BlogMediaCreate,
    BlogMediaResponse,
    BlogMediaSuccessResponse,
)
import shutil
import os
import uuid
from fastapi import Form
from typing import List

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


UPLOAD_DIR = "uploaded_imgs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/blogs/upload_blogs_media",
    response_model=BlogMediaSuccessResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_blogs_media(
    blog_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    blog = db.query(TbITBlog).filter(TbITBlog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog ID not found.",
        )

    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    media = TbITMedia(blog_id=blog_id, img=filename)
    db.add(media)
    db.commit()
    db.refresh(media)

    return {
        "message": "Image uploaded successfully",
        "data": media,
    }


@router.get(
    "/blogs/get_blogmedia",
    response_model=List[BlogMediaResponse],
    status_code=status.HTTP_200_OK,
)
def get_blog_media(request: Request, db: Session = Depends(get_db)):
    base_url = str(request.base_url).rstrip("/")
    media_list = db.query(TbITMedia).all()

    for media in media_list:
        media.img = f"{base_url}/uploaded_imgs/{media.img}"

    return media_list
