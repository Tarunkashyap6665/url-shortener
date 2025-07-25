from flask import Flask, jsonify, request, redirect, abort
from app.models import URLShortener
from app.utils import generate_short_code, is_url_reachable, is_valid_url

app = Flask(__name__)

# Create a global instance of the URL shortener
url_shortener = URLShortener()

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """
    Endpoint to shorten a URL.
    
    Expects a JSON payload with a 'url' field.
    Returns a JSON response with 'short_code' and 'short_url' fields.
    """
    # Get the request data
    data = request.get_json()
    
    # Validate request data
    if not data or 'url' not in data:
        return jsonify({
            "error": "Missing 'url' field in request"
        }), 400
    
    original_url = data['url']
    
    # Validate URL
    if not is_valid_url(original_url):
        return jsonify({
            "error": "Invalid URL provided"
        }), 400
    
    # Check if URL is reachable
    if not is_url_reachable(original_url):
        return jsonify({
            "error": "URL is not reachable"
        }), 400
    

    
    # Generate a unique short code
    max_attempts = 10
    for _ in range(max_attempts):
        short_code = generate_short_code()
        result = url_shortener.create_short_url(original_url, short_code)
        if result:
            # Successfully created short URL
            short_url = request.host_url + short_code
            return jsonify({
                "short_code": short_code,
                "short_url": short_url
            }), 201
    
    # If we reach here, we couldn't generate a unique short code after max_attempts
    return jsonify({
        "error": "Failed to generate a unique short code. Please try again."
    }), 500

@app.route('/<short_code>')
def redirect_to_url(short_code):
    """
    Endpoint to redirect to the original URL.
    
    If the short code exists, redirects to the original URL.
    If the short code doesn't exist, returns a 404 error.
    """
    original_url = url_shortener.get_original_url(short_code)
    
    if original_url:
        return redirect(original_url)
    else:
        abort(404, description="Short code not found")

@app.route('/api/stats/<short_code>')
def get_url_stats(short_code):
    """
    Endpoint to get statistics for a short URL.
    
    Returns a JSON response with 'url', 'clicks', and 'created_at' fields.
    If the short code doesn't exist, returns a 404 error.
    """
    stats = url_shortener.get_url_stats(short_code)
    
    if stats:
        return jsonify(stats)
    else:
        return jsonify({
            "error": "Short code not found"
        }), 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": str(error.description)
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "error": "Internal server error"
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)