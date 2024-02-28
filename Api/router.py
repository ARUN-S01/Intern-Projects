from model import Schema, UpdateSchema, DeleteSchema
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Body, Request
from typing import List

router = APIRouter()

@router.get("/getData", response_model=List[Schema])
async def get_data(request: Request):
    try:
        return list(request.app.database["names"].find())
    except Exception as e:
        print("Error in Retrival ", e)
        return {
            "message": "Error in Retrival", 
            "code":e.args[0]
        }
    
@router.post("/insertData")
async def insert_data(request: Request, data: Schema = Body()):
    try:
        request.app.database["names"].insert_one(jsonable_encoder(data))
        return {"message":"Insertion Success"}
    except Exception as e:
        print("Error in Inserting ", e)
        return {
            "message": "Error in Inserting", 
            "code":e.args[0]
        }

@router.put("/updateData/")
async def update_data(request: Request, data: UpdateSchema = Body()):
    try:
        data = jsonable_encoder(data)
        update_data = {k: v for k, v in data.items() if v is not None}
        request.app.database["names"].find_one_and_update(
            {"phone":update_data.get("phone")},
            {"$set":update_data})
        return {"message":"Update Success"}
    except Exception as e:
        print("Error in Updating ", e)
        return {
            "message": "Error in Updating", 
            "code":e.args[0]
        }

@router.delete("/deleteData")
async def delete_data(request: Request, data: DeleteSchema = Body()):
    try:
        request.app.database["names"].delete_one(
            jsonable_encoder(data)
        )
        return {"message": "Delete Success"}
    except Exception as e:
        print("Error in Deletetion ", e)
        return {
            "message": "Error in Delete", 
            "code":e.args[0]
        }