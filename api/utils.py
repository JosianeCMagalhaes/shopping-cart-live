import os
from pydoc import plain
import redis
import binascii

from passlib.context import CryptContext
from fastapi_mail import FastMail, MessageSchema 
from fastapi import BackgroundTasks

redis = redis.Redis.from_url('redis://')
password_context = CryptContext(schemes=['bcrypt'])

class Hash():
    def bcrypt(password):
        password_context.hash(password)
    
    def verify(plain_password, hashed_password):
        return password_context.verify(plain_password, hashed_password)