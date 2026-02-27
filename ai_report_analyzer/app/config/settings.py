import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Centralized configuration management class for application settings loaded from environment variables.

    This class provides a centralized location for accessing application-wide configuration settings
    that are loaded from environment variables using the python-dotenv library. It serves as a 
    single source of truth for sensitive configuration data such as database connections,
    API keys, and security tokens. The class uses lazy loading through os.getenv() to retrieve
    values only when accessed, which helps with performance and security by avoiding unnecessary
    exposure of sensitive information during initialization.

    Example:
        # Access database configuration
        db_url = Settings.DATABASE_URL
        
        # Access AI service API key
        api_key = Settings.GEMINI_API_KEY
        
        # Access application secret key
        secret = Settings.SECRET_KEY
    """

    DATABASE_URL = os.getenv("DATABASE_URL")
    """
    Database connection string loaded from the 'DATABASE_URL' environment variable.
    
    This attribute contains the full database connection URI including protocol, credentials,
    host, port, and database name. Common formats include PostgreSQL ('postgresql://...'),
    MySQL ('mysql://...'), or SQLite ('sqlite:///...') connection strings. The value is 
    typically None if the environment variable is not set, so consumers should handle
    potential None values appropriately.
    """

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    """
    API key for Google's Gemini AI service loaded from the 'GEMINI_API_KEY' environment variable.
    
    This attribute stores the authentication token required to access Google's Gemini AI services
    for machine learning, natural language processing, or other AI capabilities. The API key
    is sensitive information that grants access to potentially costly cloud services and should
    be protected accordingly. Returns None if the environment variable is not configured.
    """

    SECRET_KEY = os.getenv("SECRET_KEY")
    """
    Cryptographic secret key loaded from the 'SECRET_KEY' environment variable.
    
    This attribute contains a secret key used for cryptographic operations such as signing
    sessions, generating secure tokens, encrypting sensitive data, or other security-related
    functions within the application. This key should be a long, random string and kept
    strictly confidential. Returns None if the environment variable is not set, which may
    cause security vulnerabilities in applications that require this key.
    """

settings = Settings()
"""
Global instance of the Settings class providing convenient access to application configuration.

This global instance allows modules throughout the application to access configuration settings
without needing to instantiate the Settings class themselves. It provides a consistent interface
for retrieving environment-based configuration values across the entire application lifecycle.
The instance is created once during module import and remains available throughout the application's
runtime for accessing database URLs, API keys, and other sensitive configuration parameters.
"""