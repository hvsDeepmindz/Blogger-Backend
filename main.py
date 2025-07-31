from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from routes.blogRoutes import router as blog_router
from routes.blogMediaRoutes import router as blog_media_router
from routes.auth.auth import router as auth_router, verify_token
from db.database import engine
from models.blogModel import Base
from models.blogMediaModel import TbITMedia

app = FastAPI(
    title="Blogger Backend",
    description="API for managing blog data including create, read, update, delete, search, and sort features.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(
    blog_router, prefix="/api", tags=["blogs"], dependencies=[Depends(verify_token)]
)
app.include_router(
    blog_media_router,
    prefix="/api",
    tags=["blogs-media"],
    dependencies=[Depends(verify_token)],
)

Base.metadata.create_all(bind=engine)

app.mount(
    "/uploaded_imgs", StaticFiles(directory="uploaded_imgs"), name="uploaded_imgs"
)


@app.get("/")
def root():
    return JSONResponse(content={"message": "Welcome to Blogger!"})
