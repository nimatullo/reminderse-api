from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from pydantic import conset

from core.api.auth.routes import auth
from core.api.users.routes import me
from core.api.links.routes import links
from core.api.texts.routes import texts
from core.config import settings

from decouple import config

app = FastAPI()

origins = [
    "https://www.reminderse.com",
]

try:
    if config("LOCAL"):
        origins.append("http://localhost:3000")
except Exception as e:
    print("LOCAL is not set")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@AuthJWT.load_config
def get_settings():
    return settings


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth, prefix="/auth", tags=["auth"])
app.include_router(me, prefix="/me", tags=["user"])
app.include_router(links, prefix="/links", tags=["links"])
app.include_router(texts, prefix="/texts", tags=["texts"])
