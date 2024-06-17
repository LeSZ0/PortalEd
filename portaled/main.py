from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from portaled.apis import apis_router
from portaled.auth.api import auth_router
from portaled.database.db import init_db
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from portaled.utils.get_env import getenv
import portaled.error_handlers as error_handlers
from portaled.utils.errors import NotFoundError


load_dotenv("portaled/envs/dev.env")

app = FastAPI()
app.include_router(auth_router)
app.include_router(apis_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=getenv("ALLOWED_ORIGINS"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AssertionError, error_handlers.assertion_error_handler)
app.add_exception_handler(NotFoundError, error_handlers.not_found_error_handler)

init_db()
