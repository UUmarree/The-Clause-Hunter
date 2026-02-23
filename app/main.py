from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import extract

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description = "Asynchrnouos API for extracting key information and clauses from insurance policy documents using ML models.",
    docs_url="/docs",
)
@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Health check endpoint to verify that the API is running.
    """

    return {"status": "healthy", "version": settings.VERSION}

app.include_router(extract.router, prefix="/api/v1/extract", tags=["Extraction"])
