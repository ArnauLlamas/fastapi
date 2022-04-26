from fastapi import FastAPI

from .routers import auth, users
from .settings import settings
from .storage import models
from .storage.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
app.include_router(auth.router, tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/status")
def hello_world():
    return {"Hello": "World"}


if __name__ == "__main__":
    pass
