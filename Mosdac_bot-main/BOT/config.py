import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MongoDB configuration
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/'
    DATABASE_NAME = os.environ.get('DATABASE_NAME') or 'chatbot_app'
    
    # Flask settings
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    TESTING = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Chat configuration
    MAX_MESSAGE_LENGTH = 500
    MAX_CHAT_HISTORY = 100
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE = 30
    
    # CORS settings
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:8501']

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
class TestingConfig(Config):
    TESTING = True
    DATABASE_NAME = 'chatbot_test'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
