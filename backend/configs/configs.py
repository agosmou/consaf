import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABASE_URI = os.environ.get("DATABASE_URI", "DEFAULT_DATABASE_URI")
    UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")


class DevelopmentConfig(Config):
    RECAPTCHA_KEY = os.environ.get("DEV_RECAPTCHA_KEY")
    SERVER_URL = "http://localhost:5000"


class ProductionConfig(Config):
    RECAPTCHA_KEY = os.environ.get("PROD_RECAPTCHA_KEY")
    SERVER_URL = "https://OFFICIALWEBSITENAME.com"
