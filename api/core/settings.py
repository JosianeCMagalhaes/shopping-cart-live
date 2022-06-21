import ast
from pydantic import BaseSettings
from decouple import config

class Settings(BaseSettings):
    NAME_APP: str = 'Shopping Car'
    DATABASE_USER: str = ''
    DATABASE_PASSWORD: str =''
    DATABASE_HOST: str = ''
    DATABASE_NAME: str = 'luizacode.db'
    HOST='0.0.0.0'
    JWT_SECRET = config('JWT_SECRET')
    MAIL_USERNAME=config('MAIL_USERNAME')
    MAIL_PASSWORD=config('MAIL_PASSWORD')
    MAIL_FROM=config('MAIL_FROM')
    MAIL_SERVER='smtp.gmail.com'
    IS_SMTP_CONFIG=ast.literal_eval('False')
    
    
settings = Settings()