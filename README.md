# URL Shortener Service

## Overview

This is a simple URL shortening service similar to bit.ly or tinyurl. It allows you to convert long URLs into short, easy-to-share links. The service provides endpoints for shortening URLs, redirecting to original URLs, and viewing analytics for shortened URLs.

## Features

- **URL Shortening**: Convert long URLs into short 6-character codes
- **Redirection**: Automatically redirect users to the original URL when they visit the shortened link
- **Analytics**: Track usage statistics including click count and creation time
- **Thread Safety**: Handle concurrent requests properly with thread locks
- **Validation**: Ensure only valid URLs are accepted

## Tech Stack

- **Python 3.8+**: Core programming language
- **Flask**: Web framework for API endpoints
- **In-memory Storage**: No external database required

## Project Structure

```
├── .gitignore           # Git ignore file
├── NOTES.md             # Notes about AI usage in the project
├── README.md            # Project documentation
├── app/                 # Application source code
│   ├── __init__.py      # Package initializer
│   ├── main.py          # Main application entry point and API routes
│   ├── models.py        # Data models (URLShortener and URLEntry classes)
│   └── utils.py         # Utility functions (URL validation, code generation)
├── requirements.txt     # Project dependencies
└── tests/               # Test suite
    └── test_basic.py    # Basic functionality tests
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/Tarunkashyap6665/url-shortener.git

# Navigate to the project directory
cd url-shortener

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Start the application
python -m flask --app app.main run

# The API will be available at http://localhost:5000
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run tests with verbose output
python -m pytest -v
```

## API Documentation

### 1. Shorten URL

**Endpoint**: `POST /api/shorten`

**Description**: Converts a long URL into a short code.

**Request Body**:

```json
{
  "url": "https://www.example.com/very/long/url"
}
```

**Success Response** (201 Created):

```json
{
  "short_code": "abc123",
  "short_url": "http://localhost:5000/abc123"
}
```

**Error Responses**:

- 400 Bad Request: Missing URL or invalid URL format
- 400 Bad Request: URL is not reachable
- 500 Internal Server Error: Failed to generate unique short code

### 2. Redirect to Original URL

**Endpoint**: `GET /<short_code>`

**Description**: Redirects to the original URL associated with the short code.

**Success Response**: 302 Redirect to the original URL

**Error Response**: 404 Not Found if short code doesn't exist

### 3. Get URL Statistics

**Endpoint**: `GET /api/stats/<short_code>`

**Description**: Returns analytics for a shortened URL.

**Success Response** (200 OK):

```json
{
  "url": "https://www.example.com/very/long/url",
  "clicks": 5,
  "created_at": "2023-07-01T10:00:00"
}
```

**Error Response**: 404 Not Found if short code doesn't exist

## Implementation Details

### Data Structure

The URL shortener uses in-memory storage with the following components:

- **URLShortener**: Main class that manages URL mappings and provides thread-safe operations
- **URLEntry**: Class to store information about a shortened URL including original URL, click count, and creation timestamp

### Thread Safety

The implementation uses Python's `threading.RLock` to ensure thread-safe operations on the shared data structures. All operations that modify the URL mappings are protected by locks.

### URL Validation

The service performs two levels of validation:

1. **Format Validation**: Ensures the URL has a valid format with proper scheme and domain
2. **Reachability Check**: Verifies that the URL is actually reachable

### Short Code Generation

Short codes are generated as random 6-character alphanumeric strings. The system handles potential collisions by retrying code generation if a duplicate is detected.
