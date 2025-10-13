"""
Business logic services for fact-checking
"""
import httpx
import base64
import json
import logging
from typing import Dict
from mistralai import Mistral

from config import settings
from exceptions import URLFetchError, MistralAPIError, InvalidFileError, ContentTooLargeError

# Configure logging
logger = logging.getLogger(__name__)


class MistralService:
    """Service for interacting with Mistral AI API"""
    
    def __init__(self, api_key: str):
        self.client = Mistral(api_key=api_key)
        logger.info("Mistral AI client initialized")
    
    async def analyze_text(self, content: str, content_type: str) -> Dict:
        """
        Analyze text content using Mistral AI
        
        Args:
            content: The text content to analyze
            content_type: Type of content (text, webpage, etc.)
            
        Returns:
            Dictionary containing analysis results
            
        Raises:
            MistralAPIError: If the API call fails
        """
        prompt = self._create_analysis_prompt(content, content_type)
        
        try:
            logger.info(f"Analyzing {content_type} with Mistral AI")
            response = self.client.chat.complete(
                model=settings.mistral_text_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=settings.mistral_temperature,
                response_format={"type": "json_object"}
            )
            
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            logger.info(f"Analysis completed successfully for {content_type}")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Mistral AI response: {e}")
            raise MistralAPIError("Invalid JSON response from AI")
        except Exception as e:
            logger.error(f"Mistral AI API error: {e}")
            raise MistralAPIError(str(e))
    
    async def analyze_image(self, image_base64: str) -> Dict:
        """
        Analyze image using Mistral AI vision model
        
        Args:
            image_base64: Base64 encoded image
            
        Returns:
            Dictionary containing analysis results
            
        Raises:
            MistralAPIError: If the API call fails
        """
        prompt = self._create_image_analysis_prompt()
        
        try:
            logger.info("Analyzing image with Mistral AI vision model")
            response = self.client.chat.complete(
                model=settings.mistral_vision_model,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_base64}"}
                    ]
                }],
                temperature=settings.mistral_temperature,
                response_format={"type": "json_object"}
            )
            
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            logger.info("Image analysis completed successfully")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Mistral AI response: {e}")
            raise MistralAPIError("Invalid JSON response from AI")
        except Exception as e:
            logger.error(f"Mistral AI vision API error: {e}")
            raise MistralAPIError(str(e))
    
    @staticmethod
    def _create_analysis_prompt(content: str, content_type: str) -> str:
        """Create the analysis prompt for Mistral AI"""
        return f"""You are an expert fact-checker. Analyze the following {content_type} and provide a comprehensive fact-check.

Content to analyze:
{content}

Provide a detailed analysis in the following JSON format:
{{
    "rating": <number between 0-10, where 10 is completely factual>,
    "confidence": <number between 0-1 indicating your confidence in this assessment>,
    "explanation": "<brief explanation of the rating>",
    "analysis": "<detailed analysis of the content>",
    "correct_aspects": ["<list of correct or verified claims>"],
    "incorrect_aspects": ["<list of incorrect, misleading, or unverified claims>"],
    "sources": [
        {{
            "title": "<source title>",
            "url": "<source url>",
            "relevance": "<why this source is relevant>"
        }}
    ]
}}

Be thorough, objective, and provide credible sources. If you cannot verify something, mention it in the analysis."""
    
    @staticmethod
    def _create_image_analysis_prompt() -> str:
        """Create the image analysis prompt for Mistral AI"""
        return """You are an expert fact-checker. Analyze this image and fact-check any claims, text, or information visible in it.

Provide a detailed analysis in the following JSON format:
{
    "rating": <number between 0-10, where 10 is completely factual>,
    "confidence": <number between 0-1 indicating your confidence in this assessment>,
    "explanation": "<brief explanation of the rating>",
    "analysis": "<detailed analysis of the image content>",
    "correct_aspects": ["<list of correct or verified claims>"],
    "incorrect_aspects": ["<list of incorrect, misleading, or unverified claims>"],
    "sources": [
        {
            "title": "<source title>",
            "url": "<source url>",
            "relevance": "<why this source is relevant>"
        }
    ]
}

Be thorough, objective, and provide credible sources."""


class URLFetcherService:
    """Service for fetching content from URLs"""
    
    @staticmethod
    async def fetch_url_content(url: str) -> str:
        """
        Fetch content from a URL
        
        Args:
            url: The URL to fetch
            
        Returns:
            The fetched content as text
            
        Raises:
            URLFetchError: If fetching fails
        """
        try:
            logger.info(f"Fetching content from URL: {url}")
            async with httpx.AsyncClient(timeout=settings.url_timeout_seconds) as client:
                response = await client.get(url, follow_redirects=True)
                response.raise_for_status()
                
                content = response.text[:settings.max_url_content_length]
                logger.info(f"Successfully fetched {len(content)} characters from URL")
                return content
                
        except httpx.TimeoutException:
            logger.warning(f"Timeout fetching URL: {url}")
            raise URLFetchError("Request timed out")
        except httpx.HTTPStatusError as e:
            logger.warning(f"HTTP error fetching URL: {e.response.status_code}")
            raise URLFetchError(f"HTTP {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error fetching URL: {e}")
            raise URLFetchError(str(e))


class ImageProcessorService:
    """Service for processing uploaded images"""
    
    @staticmethod
    async def process_image(file_content: bytes, content_type: str) -> str:
        """
        Process and encode an uploaded image
        
        Args:
            file_content: The image file content
            content_type: The MIME type of the file
            
        Returns:
            Base64 encoded image string
            
        Raises:
            InvalidFileError: If file is not an image
            ContentTooLargeError: If file is too large
        """
        # Validate content type
        if not content_type.startswith("image/"):
            logger.warning(f"Invalid file type uploaded: {content_type}")
            raise InvalidFileError("File must be an image")
        
        # Check file size
        size_mb = len(file_content) / (1024 * 1024)
        if size_mb > settings.max_image_size_mb:
            logger.warning(f"Image too large: {size_mb:.2f}MB")
            raise ContentTooLargeError(
                f"Image size ({size_mb:.2f}MB) exceeds maximum allowed size ({settings.max_image_size_mb}MB)"
            )
        
        # Encode to base64
        logger.info(f"Processing image: {size_mb:.2f}MB")
        image_base64 = base64.b64encode(file_content).decode("utf-8")
        return image_base64

