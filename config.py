"""Flask configuration."""
from os import getenv


class Config:
    """Base config."""
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    ACCUWEATHER_API_KEY = getenv('ACCUWEATHER_API_KEY')
    if ACCUWEATHER_API_KEY is None:
        raise RuntimeError("ACCUWEATHER_API_KEY env variable should be set for the app to run!")
    ACCUWEATHER_API_BASE_URL = "http://dataservice.accuweather.com"
    HOST = '0.0.0.0'


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
