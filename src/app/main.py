"""API init"""
from fastapi import FastAPI

from .storage import models
from .storage.database import engine
from .routers import users, auth
from .settings import Settings


models.Base.metadata.create_all(bind=engine)
settings = Settings()

app = FastAPI(title=settings.app_name)
app.include_router(auth.router, tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/status")
def hello_world() -> str:
    """Retrieves a Hello world"""
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
