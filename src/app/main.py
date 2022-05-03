from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.routers import auth, users
from app.settings import settings
from app.storage.database import init_db

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)


app.include_router(auth.router, tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])


@app.on_event("startup")
def startup_event():
    init_db(settings.database_url)


@app.get("/status")
async def hello_world():
    return {"Hello": "World"}


if __name__ == "__main__":
    pass
