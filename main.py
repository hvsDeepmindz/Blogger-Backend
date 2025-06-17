from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from routes.routes import router
from db.database import engine
from models.blog import Base

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/api", tags=["blogs"])

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return JSONResponse(content={"message": "Welcome to Blogger!"})
