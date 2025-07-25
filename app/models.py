import threading
from datetime import datetime


class URLShortener:
    """
    A class to manage URL shortening operations with thread safety.
    
    This class handles storing URL mappings, tracking click counts,
    and managing URL metadata in memory.
    """
    
    def __init__(self):
        # Dictionary to store URL mappings: short_code -> URLEntry
        self.url_mappings = {}
        # Lock for thread safety
        self.lock = threading.RLock()
    
    def create_short_url(self, original_url: str, short_code: str) -> str:  
        """
        Create a new short URL mapping.
        
        Args:
            original_url (str): The original URL to shorten
            short_code (str): The generated short code
            
        Returns:
            str: The short code if successful, None if the short code already exists
        """
        with self.lock:
            if short_code in self.url_mappings:
                return None
                
            # Create a new URL entry
            entry = URLEntry(original_url)
            self.url_mappings[short_code] = entry
            return short_code
    
    def get_original_url(self, short_code: str) -> str:
        """
        Get the original URL for a short code and increment click count.
        
        Args:
            short_code (str): The short code to look up
            
        Returns:
            str or None: The original URL if found, None otherwise
        """
        with self.lock:
            entry = self.url_mappings.get(short_code)
            if entry:
                entry.increment_clicks()
                return entry.original_url
            return None
    
    def get_url_stats(self, short_code: str) -> dict | None:
        """
        Get statistics for a short URL.
        
        Args:
            short_code (str): The short code to look up
            
        Returns:
            dict or None: A dictionary with URL statistics if found, None otherwise
        """
        with self.lock:
            entry = self.url_mappings.get(short_code)
            if entry:
                return {
                    "url": entry.original_url,
                    "clicks": entry.clicks,
                    "created_at": entry.created_at.isoformat()
                }
            return None


class URLEntry:
    """
    A class to store information about a shortened URL.
    """
    
    def __init__(self, original_url: str):
        """
        Initialize a new URL entry.
        
        Args:
            original_url (str): The original URL
        """
        self.original_url = original_url
        self.clicks = 0
        self.created_at = datetime.now()
    
    def increment_clicks(self):
        """
        Increment the click count for this URL.
        """
        self.clicks += 1