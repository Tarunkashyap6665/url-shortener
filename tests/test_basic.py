import pytest
import json
from app.main import app, url_shortener
from app.utils import is_valid_url, is_url_reachable

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Clear URL mappings before each test
    url_shortener.url_mappings.clear()
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_api_health(client):
    """Test the API health endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert 'message' in data

def test_shorten_url_success(client):
    """Test successful URL shortening."""
    # Test data
    test_url = "https://artifixer.tech/ai-mock-interview"
    
    # Make request
    response = client.post(
        '/api/shorten',
        data=json.dumps({'url': test_url}),
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data
    assert len(data['short_code']) == 6  # Short code should be 6 characters
    assert data['short_url'].endswith(data['short_code'])

def test_shorten_url_invalid_url(client):
    """Test URL shortening with invalid URL."""
    # Test with invalid URL
    invalid_url = "not-a-valid-url"
    
    # Make request
    response = client.post(
        '/api/shorten',
        data=json.dumps({'url': invalid_url}),
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Invalid URL' in data['error']

def test_shorten_url_missing_url(client):
    """Test URL shortening with missing URL in request."""
    # Make request with empty body
    response = client.post(
        '/api/shorten',
        data=json.dumps({}),
        content_type='application/json'
    )
    
    # Check response
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert "Missing 'url'" in data['error']

def test_redirect_success(client):
    """Test successful redirection to original URL."""
    # First, create a short URL
    test_url = "https://artifixer.tech/e-store"
    response = client.post(
        '/api/shorten',
        data=json.dumps({'url': test_url}),
        content_type='application/json'
    )
    short_code = response.get_json()['short_code']
    
    # Now test redirection
    response = client.get(f'/{short_code}', follow_redirects=False)
    assert response.status_code == 302  # Redirect status code
    assert response.headers['Location'] == test_url

def test_redirect_not_found(client):
    """Test redirection with non-existent short code."""
    # Try to access a non-existent short code
    response = client.get('/nonexistent', follow_redirects=False)
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

def test_stats_success(client):
    """Test successful retrieval of URL statistics."""
    # First, create a short URL
    test_url = "https://www.youtube.com/"
    response = client.post(
        '/api/shorten',
        data=json.dumps({'url': test_url}),
        content_type='application/json'
    )
    short_code = response.get_json()['short_code']
    
    # Access the URL a few times to increment click count
    for _ in range(3):
        client.get(f'/{short_code}')
    
    # Now get stats
    response = client.get(f'/api/stats/{short_code}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['url'] == test_url
    assert data['clicks'] == 3
    assert 'created_at' in data

def test_stats_not_found(client):
    """Test statistics retrieval with non-existent short code."""
    # Try to get stats for a non-existent short code
    response = client.get('/api/stats/nonexistent')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

def test_url_validation():
    """Test URL validation function."""
    # Valid URLs
    assert is_valid_url("https://www.example.com") is True
    assert is_valid_url("http://example.com/path?query=value") is True
    assert is_valid_url("https://subdomain.example.co.uk/path") is True
    
    # Invalid URLs
    assert is_valid_url("not-a-url") is False
    assert is_valid_url("ftp://example.com") is False  # Not http/https
    assert is_valid_url("http://") is False  # No domain

def test_url_reachability():
    """Test URL reachability function."""
    # Test with a reachable URL
    assert is_url_reachable("https://www.google.com") is True
    assert is_url_reachable("https://www.youtube.com/") is True
    
    # Test with an unreachable URL
    assert is_url_reachable("http://nonexistent.example.com") is False
