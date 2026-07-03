from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from db import Base, SessionLocal, engine
from errors import (
    AppError,
    ConflictError,
    NotFoundError,
    UpstreamBadGatewayError,
    UpstreamUnavailableError,
    ValidationError,
)
from repositories.customers import seed_customers
from routers.customers import router as customers_router
from routers.auth import router as auth_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_customers(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Customer API",
    description="A small FastAPI service for managing customers and a few related workflows.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.exception_handler(AppError)
async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
    status_code = 500

    if isinstance(exc, NotFoundError):
        status_code = 404
    elif isinstance(exc, (ConflictError, ValidationError)):
        status_code = 400
    elif isinstance(exc, UpstreamUnavailableError):
        status_code = 503
    elif isinstance(exc, UpstreamBadGatewayError):
        status_code = 502

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )


app.include_router(customers_router)
app.include_router(auth_router)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "customer-api",
        "docs": "/docs",
    }
