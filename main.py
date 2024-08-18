from fastapi import FastAPI
from routes import router as api_router
import os
from contextlib import asynccontextmanager
from shared.cache import init_redis
import logging
from fastapi.middleware.cors import CORSMiddleware

ENV = os.getenv("ENV", "development")

local_origins = ["http://localhost", "http://localhost:3001", "*"]

origins = os.getenv("CORS_ORIGINS", "").split(",")

if ENV != "production":
    origins += local_origins


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    print("APP ENV", env)
    print(f"Running server on {host}:{port}")
    uvicorn.run(app, host=host, port=int(port), reload=reload)
