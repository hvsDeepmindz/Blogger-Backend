from pydantic import BaseModel


class BlogCreate(BaseModel):
    name: str
    desc: str


class BlogResponse(BaseModel):
    id: int
    name: str
    desc: str

    class Config:
        orm_mode = True


class BlogSuccessResponse(BaseModel):
    message: str
    data: BlogResponse
