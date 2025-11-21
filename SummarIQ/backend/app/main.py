from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1 import papers, graph, rag


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # Initialize FalkorDB connection, load models, etc.
    yield
    # Shutdown
    # Cleanup connections, etc.


app = FastAPI(
    title="SummarIQ API",
    description="Research Paper Summarization and Exploration API",
    version="1.0.0",
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

# Include routers
app.include_router(papers.router, prefix="/api/v1/papers", tags=["papers"])
app.include_router(graph.router, prefix="/api/v1/graph", tags=["graph"])
app.include_router(rag.router, prefix="/api/v1/rag", tags=["rag"])


@app.get("/")
async def root():
    return {
        "message": "SummarIQ API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

