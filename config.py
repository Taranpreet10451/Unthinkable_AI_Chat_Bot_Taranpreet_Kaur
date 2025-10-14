"""
Configuration module for AI Customer Support Bot.

This module handles all configuration settings including environment variables,
database paths, API keys, and other constants used throughout the application.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file (override system env for local dev)
load_dotenv(override=True)

# =============================================================================
# API CONFIGURATION
# =============================================================================

# Google Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validate API key
if not GEMINI_API_KEY:
    print("⚠️  Warning: GEMINI_API_KEY not found in environment variables")
    print("Please create a .env file with your Gemini API key:")
    print("GEMINI_API_KEY=your_gemini_api_key_here")

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

# SQLite Database Configuration
DATABASE_PATH = "sessions.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Database table names
SESSIONS_TABLE = "sessions"
CONVERSATIONS_TABLE = "conversations"

# =============================================================================
# FAQ DATASET CONFIGURATION
# =============================================================================

# FAQ Dataset Configuration
FAQ_DATASET_PATH = "faq_dataset.csv"
FAQ_DATASET_ENCODING = "utf-8"

# FAQ Search Configuration
FAQ_SEARCH_THRESHOLD = 1.0  # Minimum score for FAQ match
FAQ_MAX_RESULTS = 5  # Maximum number of FAQ results to return
FAQ_CONTEXT_LIMIT = 5  # Number of recent messages to include in context

# =============================================================================
# FLASK APPLICATION CONFIGURATION
# =============================================================================

# Flask Server Configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True

# Flask Application Settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# CORS Configuration (if needed for frontend)
CORS_ORIGINS = ["http://localhost:7860", "http://127.0.0.1:7860"]

# =============================================================================
# GRADIO FRONTEND CONFIGURATION
# =============================================================================

# Gradio Server Configuration
GRADIO_HOST = "0.0.0.0"
GRADIO_PORT = 7860
GRADIO_SHARE = False  # Set to True for public sharing
GRADIO_DEBUG = True

# Gradio Interface Settings
GRADIO_TITLE = "AI Customer Support Bot"
GRADIO_DESCRIPTION = "Welcome to Unthinkable Solutions AI Customer Support!"
GRADIO_THEME = "default"  # Options: default, soft, monochrome

# =============================================================================
# AI RESPONSE CONFIGURATION
# =============================================================================

# Gemini AI Model Configuration
GEMINI_MODEL_NAME = "gemini-1.5-flash"
GEMINI_MAX_TOKENS = 1000
GEMINI_TEMPERATURE = 0.7
GEMINI_TOP_P = 0.8
GEMINI_TOP_K = 40

# Response Generation Settings
MAX_RESPONSE_LENGTH = 500  # Maximum characters in AI response
MIN_RESPONSE_LENGTH = 10   # Minimum characters in AI response
RESPONSE_TIMEOUT = 30      # Timeout for AI response generation (seconds)

# =============================================================================
# SESSION MANAGEMENT CONFIGURATION
# =============================================================================

# Session Configuration
SESSION_TIMEOUT = 3600  # Session timeout in seconds (1 hour)
MAX_SESSION_MESSAGES = 100  # Maximum messages per session
SESSION_CLEANUP_INTERVAL = 300  # Cleanup interval in seconds (5 minutes)

# Conversation History Settings
MAX_CONVERSATION_HISTORY = 20  # Maximum conversation history to keep
HISTORY_CLEANUP_DAYS = 30  # Days after which to clean up old conversations

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

# Logging Settings
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "chatbot.log"
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# =============================================================================
# ERROR HANDLING CONFIGURATION
# =============================================================================

# Error Handling Settings
MAX_RETRY_ATTEMPTS = 3
RETRY_DELAY = 1  # Delay between retries in seconds
ERROR_RESPONSE_TIMEOUT = 5  # Timeout for error responses

# Custom Error Messages
ERROR_MESSAGES = {
    "api_key_missing": "API key not configured. Please check your environment variables.",
    "database_error": "Database connection error. Please try again later.",
    "ai_service_error": "AI service is temporarily unavailable. Please try again later.",
    "invalid_input": "Invalid input provided. Please check your request.",
    "rate_limit_exceeded": "Rate limit exceeded. Please wait before making another request.",
    "session_not_found": "Session not found. Please start a new conversation.",
    "timeout_error": "Request timed out. Please try again.",
}

# =============================================================================
# SECURITY CONFIGURATION
# =============================================================================

# Security Settings
ALLOWED_ORIGINS = ["http://localhost:7860", "http://127.0.0.1:7860"]
RATE_LIMIT_PER_MINUTE = 60  # Maximum requests per minute per IP
RATE_LIMIT_BURST = 10  # Burst limit for rate limiting

# Input Validation
MAX_MESSAGE_LENGTH = 1000  # Maximum characters in user message
MIN_MESSAGE_LENGTH = 1     # Minimum characters in user message
ALLOWED_MESSAGE_PATTERNS = [r"^[a-zA-Z0-9\s.,!?@#$%^&*()_+\-=\[\]{}|;':\",./<>?`~]*$"]

# =============================================================================
# PERFORMANCE CONFIGURATION
# =============================================================================

# Performance Settings
CACHE_TTL = 300  # Cache time-to-live in seconds (5 minutes)
CACHE_MAX_SIZE = 1000  # Maximum cache entries
ENABLE_RESPONSE_CACHING = True

# Database Performance
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 20
DB_POOL_TIMEOUT = 30
DB_POOL_RECYCLE = 3600

# =============================================================================
# DEVELOPMENT CONFIGURATION
# =============================================================================

# Development Settings
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "true").lower() == "true"
ENABLE_DEBUG_LOGGING = DEVELOPMENT_MODE
ENABLE_API_DOCS = DEVELOPMENT_MODE

# Testing Configuration
TEST_DATABASE_PATH = "test_sessions.db"
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_config():
    """
    Validate the configuration settings.
    
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    errors = []
    
    # Check required API key
    if not GEMINI_API_KEY:
        errors.append("GEMINI_API_KEY is required")
    
    # Check database path
    if not DATABASE_PATH:
        errors.append("DATABASE_PATH is required")
    
    # Check Flask configuration
    if not FLASK_HOST or not FLASK_PORT:
        errors.append("Flask host and port are required")
    
    # Check Gradio configuration
    if not GRADIO_HOST or not GRADIO_PORT:
        errors.append("Gradio host and port are required")
    
    # Print errors if any
    if errors:
        print("❌ Configuration validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print("✅ Configuration validation passed")
    return True

def get_database_url():
    """
    Get the complete database URL.
    
    Returns:
        str: Database URL
    """
    return DATABASE_URL

def get_gemini_config():
    """
    Get Gemini AI configuration dictionary.
    
    Returns:
        dict: Gemini configuration
    """
    return {
        "model_name": GEMINI_MODEL_NAME,
        "max_tokens": GEMINI_MAX_TOKENS,
        "temperature": GEMINI_TEMPERATURE,
        "top_p": GEMINI_TOP_P,
        "top_k": GEMINI_TOP_K,
        "api_key": GEMINI_API_KEY
    }

def get_flask_config():
    """
    Get Flask application configuration dictionary.
    
    Returns:
        dict: Flask configuration
    """
    return {
        "host": FLASK_HOST,
        "port": FLASK_PORT,
        "debug": FLASK_DEBUG,
        "secret_key": SECRET_KEY,
        "max_content_length": MAX_CONTENT_LENGTH
    }

def get_gradio_config():
    """
    Get Gradio interface configuration dictionary.
    
    Returns:
        dict: Gradio configuration
    """
    return {
        "host": GRADIO_HOST,
        "port": GRADIO_PORT,
        "share": GRADIO_SHARE,
        "debug": GRADIO_DEBUG,
        "title": GRADIO_TITLE,
        "description": GRADIO_DESCRIPTION,
        "theme": GRADIO_THEME
    }

# =============================================================================
# INITIALIZATION
# =============================================================================

if __name__ == "__main__":
    # Run configuration validation when script is executed directly
    print("🔧 AI Customer Support Bot - Configuration Validation")
    print("=" * 60)
    
    validate_config()
    
    print("\n📊 Configuration Summary:")
    print(f"  Database: {DATABASE_PATH}")
    print(f"  Flask Server: {FLASK_HOST}:{FLASK_PORT}")
    print(f"  Gradio Interface: {GRADIO_HOST}:{GRADIO_PORT}")
    print(f"  Gemini Model: {GEMINI_MODEL_NAME}")
    print(f"  Development Mode: {DEVELOPMENT_MODE}")
    print(f"  API Key Configured: {'Yes' if GEMINI_API_KEY else 'No'}")
    
    print("\n✅ Configuration module loaded successfully!")
