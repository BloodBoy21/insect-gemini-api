from fastapi import FastAPI
from routes import router as api_router
import os
from contextlib import asynccontextmanager
from shared.cache import init_redis
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        init_redis()
        yield
    finally:
        pass


app = FastAPI(
    description="API for Gemini project",
    version="0.1.0",
    title="Gemini API",
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv

    port = os.getenv("PORT", 3000)
    host = os.getenv("HOST", "0.0.0.0")
    env = os.getenv("ENV", "development")
    app = app
    reload = env == "development"
    if env == "development":
        load_dotenv()
        app = "main:app"
    uvicorn.run(app, host=host, port=int(port), reload=reload)
