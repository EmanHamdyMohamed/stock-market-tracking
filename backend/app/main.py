from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.routers import stock, user
from app.middleware.auth import authorize_token


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    connect_to_mongo()
    yield
    # Shutdown
    close_mongo_connection()


app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    debug=settings.debug,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(authorize_token)
# Include routers
app.include_router(stock.router, prefix="/stocks", tags=["stocks"])
app.include_router(user.router, prefix="/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "Welcome to Stock Market Backend API"}


@app.get("/health")
async def health():
    return {"status": "healthy", "database": "connected"}
