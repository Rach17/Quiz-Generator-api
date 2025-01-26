from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes import pdf
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting application...")
    yield
    # Shutdown
    print("Shutting down application...")

app = FastAPI(
    title="Quiz Generator API",
    description="API for generating quizzes from PDF content",
    version="0.1.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# app.include_router(quiz.router, prefix="/api/v1", tags=["quiz"])
app.include_router(pdf.router, prefix="/api/v1", tags=["pdf"])

