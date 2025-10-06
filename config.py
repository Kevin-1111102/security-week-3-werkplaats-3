from datetime import timedelta
import os


class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["cookies", "headers"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_VERIFY_SUB = False