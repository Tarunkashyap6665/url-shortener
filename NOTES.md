# AI Usage Notes

## Tools Used
- ChatGPT

## Usage Details

### URL Pattern Validation Regex
ChatGPT was used to create the regular expression pattern for additional URL validation in `utils.py`. This regex helps validate common URL patterns to ensure the URLs being shortened are properly formatted.

```python
# Additional validation for common URL patterns
url_pattern = re.compile(
    r'^(?:http|https)://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
    r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
```

### Function Docstrings
ChatGPT was used to generate docstrings for functions in the codebase, providing clear documentation of function purposes, parameters, and return values.

### README File
ChatGPT was used to assist in creating the README.md file, helping to structure and format the documentation for the URL shortener application.