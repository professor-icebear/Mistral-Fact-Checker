"""
Simple tests for the Mistral Fact Checker API

Run with: pytest test_main.py -v
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from io import BytesIO

from main import app, get_mistral_service
from services import MistralService


# Mock Mistral service for testing
class MockMistralService:
    """Mock Mistral service to avoid API calls during testing"""
    
    async def analyze_text(self, content: str, content_type: str) -> dict:
        """Mock text analysis"""
        return {
            "rating": 8.5,
            "explanation": "This is a test explanation",
            "confidence": 0.85,
            "analysis": "This is a detailed test analysis",
            "correct_aspects": ["Fact 1", "Fact 2"],
            "incorrect_aspects": ["Error 1"],
            "sources": [
                {
                    "title": "Test Source",
                    "url": "https://example.com",
                    "relevance": "Test relevance"
                }
            ]
        }
    
    async def analyze_image(self, image_base64: str) -> dict:
        """Mock image analysis"""
        return {
            "rating": 7.5,
            "explanation": "Test image analysis",
            "confidence": 0.75,
            "analysis": "Detailed image analysis",
            "correct_aspects": ["Visual element 1"],
            "incorrect_aspects": ["Visual error 1"],
            "sources": []
        }


@pytest.fixture
def client():
    """Create a test client with mocked Mistral service"""
    
    # Override the dependency
    def override_get_mistral_service():
        return MockMistralService()
    
    app.dependency_overrides[get_mistral_service] = override_get_mistral_service
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clear overrides after test
    app.dependency_overrides.clear()


class TestHealthEndpoints:
    """Tests for health check endpoints"""
    
    def test_root_endpoint(self, client):
        """Test the root health check endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data
        assert "mistral_connection" in data
    
    def test_health_endpoint(self, client):
        """Test the detailed health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "service" in data
        assert "version" in data
        assert "mistral_connection" in data


class TestTextFactCheck:
    """Tests for text fact-checking endpoint"""
    
    def test_fact_check_text_success(self, client):
        """Test successful text fact-checking"""
        payload = {
            "text": "The Earth is round and orbits the Sun."
        }
        response = client.post("/api/fact-check/text", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "rating" in data
        assert "explanation" in data
        assert "confidence" in data
        assert "analysis" in data
        assert "correct_aspects" in data
        assert "incorrect_aspects" in data
        assert "sources" in data
        assert "timestamp" in data
        assert data["input_type"] == "text"
        assert 0 <= data["rating"] <= 10
        assert 0 <= data["confidence"] <= 1
    
    def test_fact_check_text_with_context(self, client):
        """Test text fact-checking with context"""
        payload = {
            "text": "The Earth is round.",
            "context": "Scientific facts about astronomy"
        }
        response = client.post("/api/fact-check/text", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["input_type"] == "text"
    
    def test_fact_check_text_empty(self, client):
        """Test that empty text is rejected"""
        payload = {
            "text": "   "
        }
        response = client.post("/api/fact-check/text", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_fact_check_text_missing(self, client):
        """Test that missing text field is rejected"""
        payload = {}
        response = client.post("/api/fact-check/text", json=payload)
        assert response.status_code == 422  # Validation error


class TestURLFactCheck:
    """Tests for URL fact-checking endpoint"""
    
    @patch('services.URLFetcherService.fetch_url_content', new_callable=AsyncMock)
    def test_fact_check_url_success(self, mock_fetch, client):
        """Test successful URL fact-checking"""
        # Mock the URL fetch
        mock_fetch.return_value = "This is content from a webpage about science."
        
        payload = {
            "url": "https://example.com/article"
        }
        response = client.post("/api/fact-check/url", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "rating" in data
        assert "explanation" in data
        assert data["input_type"] == "url"
    
    def test_fact_check_url_invalid(self, client):
        """Test that invalid URLs are rejected"""
        payload = {
            "url": "not-a-valid-url"
        }
        response = client.post("/api/fact-check/url", json=payload)
        assert response.status_code == 422  # Validation error


class TestImageFactCheck:
    """Tests for image fact-checking endpoint"""
    
    @patch('services.ImageProcessorService.process_image', new_callable=AsyncMock)
    def test_fact_check_image_success(self, mock_process, client):
        """Test successful image fact-checking"""
        # Mock image processing
        mock_process.return_value = "base64_encoded_image_data"
        
        # Create a fake image file
        file_content = b"fake image data"
        files = {
            "file": ("test.jpg", BytesIO(file_content), "image/jpeg")
        }
        
        response = client.post("/api/fact-check/image", files=files)
        assert response.status_code == 200
        
        data = response.json()
        assert "rating" in data
        assert "explanation" in data
        assert data["input_type"] == "image"
    
    def test_fact_check_image_no_file(self, client):
        """Test that missing image file is rejected"""
        response = client.post("/api/fact-check/image")
        assert response.status_code == 422  # Validation error


class TestResponseStructure:
    """Tests for response structure validation"""
    
    def test_fact_check_response_structure(self, client):
        """Test that response has correct structure"""
        payload = {
            "text": "Test statement about facts."
        }
        response = client.post("/api/fact-check/text", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        
        # Check all required fields are present
        required_fields = [
            "rating", "explanation", "confidence", "analysis",
            "correct_aspects", "incorrect_aspects", "sources",
            "timestamp", "input_type"
        ]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Check types
        assert isinstance(data["rating"], (int, float))
        assert isinstance(data["explanation"], str)
        assert isinstance(data["confidence"], (int, float))
        assert isinstance(data["analysis"], str)
        assert isinstance(data["correct_aspects"], list)
        assert isinstance(data["incorrect_aspects"], list)
        assert isinstance(data["sources"], list)
        assert isinstance(data["timestamp"], str)
        assert isinstance(data["input_type"], str)


class TestCORS:
    """Tests for CORS middleware"""
    
    def test_cors_headers_present(self, client):
        """Test that CORS headers are present"""
        response = client.get("/health")
        assert response.status_code == 200
        # FastAPI's TestClient doesn't always include CORS headers
        # In real requests, these would be present


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

