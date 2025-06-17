from pydantic import BaseModel


class BlogMediaCreate(BaseModel):
    blog_id: int


class BlogMediaResponse(BaseModel):
    id: int
    blog_id: int
    img: str

    class Config:
        orm_mode = True


class BlogMediaSuccessResponse(BaseModel):
    message: str
    data: BlogMediaResponse
