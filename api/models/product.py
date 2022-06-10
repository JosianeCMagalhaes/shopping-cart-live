import peewee
from db.database import database


class Product(peewee.Model):
    name = peewee.CharField(max_length=100)
    description = peewee.TextField()
    price = peewee.DecimalField(max_digits=10, decimal_places=2)
    weight = peewee.DecimalField()
    code = peewee.CharField()
    
    class Meta:
        db = database
    
    