from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from db import Base, SessionLocal, engine
from errors import AppError
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
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
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
