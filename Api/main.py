from router import router as DataRouter
from dotenv import dotenv_values
from pymongo import MongoClient
from fastapi import FastAPI


app = FastAPI()
cred = dotenv_values(".env")

@app.on_event("startup")
def db_start():
    try:
        app.client = MongoClient(cred["host"], int(cred["port"]))
        app.database = app.client[cred["db"]]
        print("DB Connected")
    except Exception as e:
        print("Error in Db Connection ", e)
    
@app.on_event("shutdown")
def db_stop():
    try:
        app.client.close()
        print("DB Closed")
    except Exception as e:
        print("Error in DB closure ", e)

app.include_router(DataRouter, prefix="/api")