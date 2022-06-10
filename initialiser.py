from api.db import database
from api.db.database import DB_STATE_DEFAULT
from api.models.customer import Customer

database.database.connect()
database.database.create_tables()
database.database.close()