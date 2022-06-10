import peewee
from contextvars import Context, ContextVar
from fastapi import Depends
from api.core.settings import settings

DB_STATE_DEFAULT = {'closed': None,
                    'conn': None,
                    'ctx': None,
                    'transaction': None}

DB_STATE = ContextVar('db_state', default=DB_STATE_DEFAULT.copy())


class ConnectState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__('_state', DB_STATE)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value
    
    def __getattr__(self, name):
        return self._state.get()[name]
    

database = peewee.SqliteDatabase(settings.DATABASE_NAME, check_same_thread=False)
database._state = ConnectState()

async def reset_database_state():
    database._state._state.set(DB_STATE_DEFAULT.copy())
    database._state.reset()


def get_database():
    try:
        database.connect()
        yield
    finally:
        if not database.is_closed():
            database.close()
