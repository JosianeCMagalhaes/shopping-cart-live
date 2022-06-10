from fastapi import FastAPI
from core.settings import settings

# app = FastAPI(
#     title='Shopping Car',
#     description="",
#     version=""
# )

app = FastAPI(
    title=settings.NAME_APP
)

@app.get("/")
def read_api():
    return {'Welcome': 'Eric'}