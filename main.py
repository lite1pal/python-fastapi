from fastapi import FastAPI
from routers.customers import router as customers_router

app = FastAPI()
app.include_router(customers_router)


@app.get("/")
def health_check():
    return {"status": "ok"}
