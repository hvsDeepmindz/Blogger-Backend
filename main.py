from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from routes.blogRoutes import router as blog_router
from routes.blogMediaRoutes import router as blog_media_router
from db.database import engine
from models.blogModel import Base
from models.blogMediaModel import TbITMedia

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(blog_router, prefix="/api", tags=["blogs"])
app.include_router(blog_media_router, prefix="/api", tags=["blogs-media"])

Base.metadata.create_all(bind=engine)

app.mount(
    "/uploaded_imgs", StaticFiles(directory="uploaded_imgs"), name="uploaded_imgs"
)


@app.get("/")
def root():
    return JSONResponse(content={"message": "Welcome to Blogger!"})
