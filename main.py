from fastapi import FastAPI
from routers.customers import router as customers_router

app = FastAPI(
    title="Customer API",
    description="A small FastAPI service for managing customers and a few related workflows.",
    version="0.1.0",
)
app.include_router(customers_router)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "customer-api",
        "docs": "/docs",
    }
