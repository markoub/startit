"""
Tests for the main FastAPI application
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint returns 200 and correct response"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["message"] == "TicketConnect API is running"
    assert data["version"] == "1.0.0"

def test_root_endpoint():
    """Test the root endpoint returns correct information"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["docs"] == "/docs"
    assert data["health"] == "/health"

def test_docs_endpoint():
    """Test that the docs endpoint is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_redoc_endpoint():
    """Test that the redoc endpoint is accessible"""
    response = client.get("/redoc")
    assert response.status_code == 200

def test_openapi_json():
    """Test that the OpenAPI JSON is accessible"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "TicketConnect API"
    assert data["info"]["version"] == "1.0.0" 