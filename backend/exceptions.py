"""
Custom exceptions for the Mistral Fact Checker API
"""
from fastapi import HTTPException, status


class FactCheckerException(HTTPException):
    """Base exception for fact checker errors"""
    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(status_code=status_code, detail=detail)


class URLFetchError(FactCheckerException):
    """Exception raised when URL content cannot be fetched"""
    def __init__(self, detail: str):
        super().__init__(
            detail=f"Failed to fetch URL content: {detail}",
            status_code=status.HTTP_400_BAD_REQUEST
        )


class MistralAPIError(FactCheckerException):
    """Exception raised when Mistral AI API fails"""
    def __init__(self, detail: str):
        super().__init__(
            detail=f"Mistral AI analysis failed: {detail}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class InvalidFileError(FactCheckerException):
    """Exception raised when uploaded file is invalid"""
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class ContentTooLargeError(FactCheckerException):
    """Exception raised when content exceeds size limits"""
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        )

