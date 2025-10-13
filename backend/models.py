"""
Pydantic models for request and response validation
"""
from pydantic import BaseModel, HttpUrl, Field, field_validator
from typing import List, Optional


class TextFactCheckRequest(BaseModel):
    """Request model for text fact-checking"""
    text: str = Field(..., min_length=1, max_length=10000, description="Text content to fact-check")
    context: Optional[str] = Field(None, max_length=1000, description="Optional context for the text")
    
    @field_validator('text')
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Text cannot be empty or whitespace only')
        return v.strip()


class URLFactCheckRequest(BaseModel):
    """Request model for URL fact-checking"""
    url: HttpUrl = Field(..., description="URL to fetch and fact-check")


class Source(BaseModel):
    """Source information model"""
    title: str = Field(..., description="Title of the source")
    url: str = Field(..., description="URL of the source")
    relevance: str = Field(..., description="Why this source is relevant")


class FactCheckResponse(BaseModel):
    """Response model for fact-check results"""
    rating: float = Field(..., ge=0, le=10, description="Accuracy rating from 0-10")
    explanation: str = Field(..., description="Brief explanation of the rating")
    confidence: float = Field(..., ge=0, le=1, description="AI confidence level from 0-1")
    analysis: str = Field(..., description="Detailed analysis of the content")
    correct_aspects: List[str] = Field(default_factory=list, description="List of correct aspects")
    incorrect_aspects: List[str] = Field(default_factory=list, description="List of incorrect aspects")
    sources: List[Source] = Field(default_factory=list, description="List of sources")
    timestamp: str = Field(..., description="ISO timestamp of the analysis")
    input_type: str = Field(..., description="Type of input: text, url, or image")


class HealthCheckResponse(BaseModel):
    """Response model for health check"""
    status: str
    service: str
    version: str
    mistral_connection: str

