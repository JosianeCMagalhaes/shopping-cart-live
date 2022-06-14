from lib2to3.pytree import Base
from pydantic import BaseSettings

class Settings(BaseSettings):
    NAME_APP: str = 'Shopping Car'
    DATABASE_USER: str = ''
    DATABASE_PASSWORD: str =''
    DATABASE_HOST: str = ''
    DATABASE_NAME: str = 'luizacode.db'
    HOST='0.0.0.0'
    
    
settings = Settings()