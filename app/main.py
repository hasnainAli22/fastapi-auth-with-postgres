from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import posts, user
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(posts.router)
app.include_router(user.router)

@app.get('/')
def read_docs():
    return {'message':'Welcome to the FastAPI'}