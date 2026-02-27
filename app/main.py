import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from .error_handlers import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from .config import settings
from .middleware import logging_middleware
from .routes import router

app = FastAPI(
    title="Backend Aula",
    description="Backend para aula da Vassouras 5° período.",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

origins = ["*"] if settings.ENV == "development" else settings.ALLOWED_ORIGINS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def healthcheck():
    return {"status": "Ok"}


if "__main__" == __name__:
    uvicorn.run(app, host="0.0.0.0", port=4000)
