import sys
import os
import pytest

def setup_module():
    """Setup module for testing"""
    # Add backend directory to Python path
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)

@pytest.fixture
def client():
    """Create test client fixture"""
    setup_module()
    
    from fastapi.testclient import TestClient
    from main import app
    
    return TestClient(app)

def test_read_root(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "DevOps Dashboard API"

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_system_metrics(client):
    """Test system metrics endpoint"""
    response = client.get("/system/metrics")
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields
    required_fields = [
        "cpu_percent", 
        "memory_total", 
        "memory_used", 
        "memory_percent",
        "disk_total", 
        "disk_used", 
        "disk_percent", 
        "timestamp"
    ]
    
    for field in required_fields:
        assert field in data, f"Field '{field}' missing from response"
    
    # Check data types
    assert isinstance(data["cpu_percent"], (int, float))
    assert isinstance(data["memory_total"], int)
    assert isinstance(data["memory_used"], int)
    assert isinstance(data["memory_percent"], (int, float))

def test_prometheus_metrics(client):
    """Test prometheus metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
