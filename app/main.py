from fastapi import FastAPI
import uvicorn

from .routes import router

app = FastAPI(
    title="Backend Aula",
    description="Backend para aula da Vassouras",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(router)

@app.get("/health")
async def healthcheck():
    return {"status":"Ok"}


if "__main__" == __name__:
    uvicorn.run(app, host="0.0.0.0", port=4000)