"""
Mistral Fact Checker API
FastAPI backend for fact-checking images, links, and text using Mistral AI

This module provides REST API endpoints for fact-checking various types of content
using Mistral AI's language models.
"""
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncGenerator

from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from models import (
    TextFactCheckRequest,
    URLFactCheckRequest,
    FactCheckResponse,
    HealthCheckResponse,
    Source
)
from services import MistralService, URLFetcherService, ImageProcessorService
from exceptions import FactCheckerException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global service instances
mistral_service: MistralService = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    global mistral_service
    logger.info("Starting Mistral Fact Checker API...")
    logger.info(f"Environment: {settings.api_version}")
    
    try:
        mistral_service = MistralService(api_key=settings.mistral_api_key)
        logger.info("✅ Mistral AI service initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Mistral AI service: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Mistral Fact Checker API...")


# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(FactCheckerException)
async def fact_checker_exception_handler(request, exc: FactCheckerException):
    """Handle custom fact checker exceptions"""
    logger.error(f"FactCheckerException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# Dependency injection
def get_mistral_service() -> MistralService:
    """Dependency to get Mistral service instance"""
    return mistral_service


# API Routes

@app.get("/", response_model=HealthCheckResponse)
async def root():
    """
    Health check endpoint
    
    Returns basic service information and health status
    """
    return HealthCheckResponse(
        status="healthy",
        service=settings.api_title,
        version=settings.api_version,
        mistral_connection="connected" if mistral_service else "disconnected"
    )


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Detailed health check endpoint
    
    Checks the health of the service and its dependencies
    """
    mistral_status = "connected" if mistral_service else "disconnected"
    
    return HealthCheckResponse(
        status="healthy" if mistral_status == "connected" else "unhealthy",
        service=settings.api_title,
        version=settings.api_version,
        mistral_connection=mistral_status
    )


@app.post("/api/fact-check/text", response_model=FactCheckResponse, tags=["Fact Checking"])
async def fact_check_text(
    request: TextFactCheckRequest,
    service: MistralService = Depends(get_mistral_service)
):
    """
    Fact-check text content
    
    Analyzes the provided text and returns a comprehensive fact-check report
    including rating, confidence level, analysis, and sources.
    
    Args:
        request: Text fact-check request containing text and optional context
        service: Injected Mistral service instance
        
    Returns:
        FactCheckResponse with complete analysis
        
    Raises:
        MistralAPIError: If the AI analysis fails
    """
    logger.info("Processing text fact-check request")
    
    # Prepare content
    content = request.text
    if request.context:
        content = f"Context: {request.context}\n\nContent: {request.text}"
    
    # Analyze with Mistral AI
    result = await service.analyze_text(content, "text")
    
    # Build response
    response = _build_response(result, "text")
    logger.info(f"Text fact-check completed with rating: {response.rating}")
    
    return response


@app.post("/api/fact-check/url", response_model=FactCheckResponse, tags=["Fact Checking"])
async def fact_check_url(
    request: URLFactCheckRequest,
    service: MistralService = Depends(get_mistral_service)
):
    """
    Fact-check content from a URL
    
    Fetches content from the provided URL and performs a fact-check analysis.
    
    Args:
        request: URL fact-check request
        service: Injected Mistral service instance
        
    Returns:
        FactCheckResponse with complete analysis
        
    Raises:
        URLFetchError: If the URL cannot be fetched
        MistralAPIError: If the AI analysis fails
    """
    logger.info(f"Processing URL fact-check request: {request.url}")
    
    # Fetch URL content
    content = await URLFetcherService.fetch_url_content(str(request.url))
    
    # Analyze with Mistral AI
    result = await service.analyze_text(content, "webpage")
    
    # Build response
    response = _build_response(result, "url")
    logger.info(f"URL fact-check completed with rating: {response.rating}")
    
    return response


@app.post("/api/fact-check/image", response_model=FactCheckResponse, tags=["Fact Checking"])
async def fact_check_image(
    file: UploadFile = File(..., description="Image file to fact-check"),
    service: MistralService = Depends(get_mistral_service)
):
    """
    Fact-check an image
    
    Analyzes an uploaded image for any claims, text, or information that can be fact-checked.
    Uses Mistral AI's vision model (Pixtral).
    
    Args:
        file: Uploaded image file
        service: Injected Mistral service instance
        
    Returns:
        FactCheckResponse with complete analysis
        
    Raises:
        InvalidFileError: If the file is not a valid image
        ContentTooLargeError: If the image is too large
        MistralAPIError: If the AI analysis fails
    """
    logger.info(f"Processing image fact-check request: {file.filename}")
    
    # Read and process image
    image_data = await file.read()
    image_base64 = await ImageProcessorService.process_image(
        image_data,
        file.content_type
    )
    
    # Analyze with Mistral AI vision
    result = await service.analyze_image(image_base64)
    
    # Build response
    response = _build_response(result, "image")
    logger.info(f"Image fact-check completed with rating: {response.rating}")
    
    return response


# Helper functions

def _build_response(result: dict, input_type: str) -> FactCheckResponse:
    """
    Build a FactCheckResponse from Mistral AI result
    
    Args:
        result: Dictionary containing analysis results from Mistral AI
        input_type: Type of input that was analyzed
        
    Returns:
        Structured FactCheckResponse object
    """
    return FactCheckResponse(
        rating=result.get("rating", 5.0),
        explanation=result.get("explanation", "No explanation provided"),
        confidence=result.get("confidence", 0.5),
        analysis=result.get("analysis", "No analysis available"),
        correct_aspects=result.get("correct_aspects", []),
        incorrect_aspects=result.get("incorrect_aspects", []),
        sources=[Source(**source) for source in result.get("sources", [])],
        timestamp=datetime.utcnow().isoformat(),
        input_type=input_type
    )


# Entry point for running the server directly
if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level="info"
    )
