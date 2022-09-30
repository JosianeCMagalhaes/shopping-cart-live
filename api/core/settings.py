import ast
from pydantic import BaseSettings
from decouple import config


class Settings(BaseSettings):
    NAME_APP: str = 'Shopping Cart'
    DATABASE_HOST: str = config('DATABASE_HOST')
    HOST: str = config('HOST')
    PORT: int = config('PORT')
    JWT_SECRET = config('JWT_SECRET')
    MAIL_USERNAME = config('MAIL_USERNAME')
    MAIL_PASSWORD = config('MAIL_PASSWORD')
    MAIL_FROM = config('MAIL_FROM')
    MAIL_SERVER = config('MAIL_SERVER')
    IS_SMTP_CONFIG = ast.literal_eval(config('IS_SMTP_CONFIG'))
    EXPIRED_CART= config('EXPIRED_CART')
    REDIS_URI=config('REDIS_URI')
    REDIS_HOST=config('REDIS_HOST')
    REDIS_PORT=config('REDIS_PORT')


settings = Settings()
