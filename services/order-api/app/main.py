
from dotenv import load_dotenv
from fastapi import FastAPI
import logging
import sys
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import config
from app.httpServer.main import router


load_dotenv()
logger = logging.getLogger("my_app")
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
        force=True,  # important
    )
configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting...")
    yield
    logger.info("Application shutting down...")

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    print("PRINT WORKS")
    logger.info("This log will definitely show up in your terminal!")
    return {"Hello": "World"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.http.cors_allow_origins,
    allow_methods=config.http.cors_allow_methods,
    allow_headers=config.http.cors_allow_headers,
    allow_credentials=config.http.cors_allow_credentials,
)


app.include_router(router)