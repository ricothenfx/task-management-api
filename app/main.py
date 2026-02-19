from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.session import engine, Base
import app.models #load all models into Base.metadata

from app.api.v1.router import api_router
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    Base.metadata.create_all(bind=engine)
    yield
    # shutdown (optional)

app = FastAPI(
    lifespan=lifespan,
    title="Task Management API",
    description="""
A secure Task Management REST API built with FastAPI.

Features:
- JWT Authentication
- Object-Level Authorization
- PostgreSQL + SQLAlchemy
- Clean Architecture (Service + Repository pattern)

This project is part of backend portfolio development.
    """,
    version="1.0.0",
    contact={
        "name": "Rico",
        "email": "ricothenfx@gmail.com",
        "url": "https://github.com/ricothenfx"
    },
    docs_url="/docs",
    redoc_url="/redoc"
)
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "project": "TASK MANAGEMENT API",
        "version": "1.0.0",
        "description": "A secure task management REST API built with FastAPI.",
        "features": [
            "JWT Authentication",
            "User Registration & Login",
            "Task CRUD Operations",
            "Object-Level Authorization",
            "PostgreSQL + SQLAlchemy"
        ],
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000))
    )