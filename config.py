# config.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from a .env file


class Config:
    OAUTH2_AUTHORIZATION_URL = os.getenv(
        'OAUTH2_AUTHORIZATION_URL',
        'https://accounts.google.com/o/oauth2/v2/auth'
    )
    OAUTH2_TOKEN_URL = os.getenv(
        'OAUTH2_TOKEN_URL',
        'https://oauth2.googleapis.com/token'
    )
    CLIENT_ID = os.getenv('OAUTH2_CLIENT_ID')
    CLIENT_SECRET = os.getenv('OAUTH2_CLIENT_SECRET')
    REDIRECT_URI = os.getenv(
        'OAUTH2_REDIRECT_URI', 'http://localhost:8000'
    )
