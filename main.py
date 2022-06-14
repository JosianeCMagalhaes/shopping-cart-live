from imp import reload
import uvicorn
from fastapi import FastAPI
from api.routers import api_router
from api.core import settings
from api.server.database import connect_db, close_conn_db


app = FastAPI(title=settings.NAME_APP)

# add conection database
app.add_event_handler('startup', connect_db)
app.add_event_handler('shutdown', close_conn_db)

# add routes
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=8000, reload=True)