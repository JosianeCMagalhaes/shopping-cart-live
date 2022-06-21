import os
import binascii
import redis
from fastapi import BackgroundTasks, HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from passlib.context import CryptContext
from api.core.settings import settings
from api.server.validation import validate_object_id

redis = redis.Redis.from_url(settings.REDIS_URI)
pwd_encrypted = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def encrypt(self, password):
        return pwd_encrypted.hash(password)

    def verify(self, password, password_encrypted):
        return pwd_encrypted.verify(password, password_encrypted)

async def get_field_or_404(id, collection, field):
    data = await collection.find_one({'_id': validate_object_id(id)})
    if data:
        return fix_id(data)
    raise HTTPException(status_code=404, detail=f'{field} not found')

def fix_id(data):
    if data.get('_id', False):
        data['_id'] = str(data['_id'])
        return data
    raise ValueError(f'_id not found!')

def send_register(id, email, background_tasks: BackgroundTasks):
    delete_token_redis(id, 'register')
    token = token_add_redis(id=id, mode='register')
    if settings.IS_SMTP_CONFIG:
        send_email(email=email, token=token, background_tasks=background_tasks)
    return token

def send_email(email, token, background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject='Ativação de Conta',
        recipients=[email],
        body=''.join(token)
    )

    config_email = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=587,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_TLS=True,
        MAIL_SSL=False
    )

    conf = FastMail(config_email)

    background_tasks.add_task(conf.send_message, message)

def token_add_redis(id, mode):
    token = _generate_code()
    name = f'{id}_{mode.lower()}'
    redis.set(name=name, value=token, ex=14400)
    return token


def delete_token_redis(id, mode):
    name = f'{id}_{mode.lower()}'
    return redis.delete(name)

def get_from_redis(id, mode):
    name = f'{id}_{mode.lower()}'
    return redis.get(name=name)

def _generate_code():
    return binascii.hexlify(os.urandom(20)).decode('utf-8')
