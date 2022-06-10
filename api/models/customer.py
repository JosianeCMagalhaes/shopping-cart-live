import peewee
from api.db.database import database


class Customer(peewee.Model):
    name = peewee.CharField()
    email = peewee.CharField(unique=True, index=True)
    password = peewee.CharField()
    is_active = peewee.BooleanField(default=True)
    is_adm = peewee.BooleanField(default=False)
    
    class Meta:
        db = database
