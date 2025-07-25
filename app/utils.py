import random
import string
import re
from urllib.parse import urlparse
import requests


def generate_short_code(length: int = 6) -> str:    
    """
    Generate a random alphanumeric short code of specified length.
    
    Args:
        length (int): Length of the short code to generate. Default is 6.
        
    Returns:
        str: A random alphanumeric string of specified length.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def is_valid_url(url:str)->bool:
    """
    Validate if the given string is a valid URL.
    
    Args:
        url (str): URL to validate.
        
    Returns:
        bool: True if URL is valid, False otherwise.
    """
    try:
        # Check if URL has a scheme and netloc
        result = urlparse(url)
        valid_scheme = result.scheme in ('http', 'https')
        valid_netloc = result.netloc != ''
        
        # Additional validation for common URL patterns
        url_pattern = re.compile(
            r'^(?:http|https)://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
            r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        pattern_match = bool(url_pattern.match(url))
        
        return valid_scheme and valid_netloc and pattern_match
    except Exception:
        return False
    
def is_url_reachable(url: str) -> bool:
    """
    Check if the given URL is reachable.
    
    Args:
        url (str): URL to check.
        
    Returns:
        bool: True if URL is reachable, False otherwise.
    """
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code < 400
    except requests.RequestException:
        return False
