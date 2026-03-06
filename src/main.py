from fastapi import FastAPI
from models.user import User
from db import users_collection

app = FastAPI()

@app.post("/users")
async def create_user(user: User):
    result = await users_collection.insert_one(user.dict())
    return {"id": str(result.inserted_id)}

@app.get("/users")
async def get_users():
    users = []
    async for user in users_collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

@app.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user.dict()}
    )
    return {"message": "updated"}

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    await users_collection.delete_one({"_id": ObjectId(user_id)})
    return {"message": "deleted"}