from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.blogModel import TbITBlog
from schemas.blogSchemas import BlogCreate, BlogResponse, BlogSuccessResponse
from typing import List

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/blogs/create_blog",
    response_model=BlogSuccessResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_blog(blog: BlogCreate, db: Session = Depends(get_db)):
    existing_blog = db.query(TbITBlog).filter(TbITBlog.name == blog.name).first()
    if existing_blog:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Blog already exists. Name should be unique.",
        )
    db_blog = TbITBlog(name=blog.name, desc=blog.desc)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return {
        "message": "Blog created successfully",
        "data": db_blog,
    }


@router.get(
    "/blogs/get_all_blogs",
    response_model=List[BlogResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(TbITBlog).all()
    return blogs


@router.put(
    "/blogs/update_blog/{blog_id}",
    response_model=BlogSuccessResponse,
    status_code=status.HTTP_200_OK,
)
def update_blog(blog_id: int, blog: BlogCreate, db: Session = Depends(get_db)):
    db_blog = db.query(TbITBlog).filter(TbITBlog.id == blog_id).first()
    if not db_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog does not exist.",
        )
    db_blog.name = blog.name
    db_blog.desc = blog.desc
    db.commit()
    db.refresh(db_blog)
    return {
        "message": "Blog updated successfully",
        "data": db_blog,
    }


@router.delete(
    "/blogs/delete_blog/{blog_id}",
    status_code=status.HTTP_200_OK,
)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    db_blog = db.query(TbITBlog).filter(TbITBlog.id == blog_id).first()
    if not db_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog does not exist.",
        )
    db.delete(db_blog)
    db.commit()
    return {"message": "Blog deleted successfully"}
