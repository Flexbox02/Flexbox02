import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SNIPE_IT_URL = os.getenv('SNIPE_IT_URL')
    SNIPE_IT_TOKEN = os.getenv('SNIPE_IT_TOKEN')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.SNIPE_IT_URL:
            raise ValueError("SNIPE_IT_URL is required")
        if not cls.SNIPE_IT_TOKEN:
            raise ValueError("SNIPE_IT_TOKEN is required")
        return True