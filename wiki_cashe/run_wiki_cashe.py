import os, sys
sys.path.insert(0, os.path.abspath(__file__ + "/../../"))
from fastapi import FastAPI
from wiki_cashe.db.data import Data
from wiki_cashe.wiki.wiki import wiki_entity
from wiki_cashe.config.config import settings
from wiki_cashe.models.wiki_models import Wiki

db = Data.data_pipeline(settings=settings)
app = FastAPI(title='Service')

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.close()

@app.get("/")
async def root():
    return {"message": "API for providing various functions. Pls see :  http://host:port/docs or http://host:port/redoc"}

@app.get('/wiki/{searched_title}', response_model=Wiki)
async def wiki(searched_title:str):
    db_value = await db.get_value(key=searched_title)
    if len(db_value.keys()) > 1:
        wiki_value = db_value
    else:
        wiki_value = await wiki_entity(search_term=searched_title)
        wiki_value_dict = dict(wiki_value)
        await db.set_value(key=searched_title, value=wiki_value_dict)
    return wiki_value
