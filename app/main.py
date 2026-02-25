from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def healthcheck():
    return {"status":"Ok"}


if "__main__" == __name__:
    uvicorn.run(app, host="0.0.0.0", port=5000)