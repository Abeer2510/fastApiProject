
from fastapi import FastAPI
from .database import engine
from . import models
from .database import engine



models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title = "CRUD app for posts",
    description="Yippee"
)

from .routers import posts
from .routers import sqlalchemy
from .routers import users
from .routers import auth

app.include_router(posts.router)
app.include_router(sqlalchemy.router)
app.include_router(users.router)
app.include_router(auth.router)




