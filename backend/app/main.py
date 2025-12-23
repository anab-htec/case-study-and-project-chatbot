from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.dependencies import weaviate_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Open the gRPC connection pool
    await weaviate_manager.connect() 
    yield
    # Shutdown: Gracefully close connections
    await weaviate_manager.disconnect()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)