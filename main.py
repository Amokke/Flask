import uvicorn as uvicorn
from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


users = []


@app.get("/")
async def receive():
    return {"user_list": users}


@app.get("/users/{user_id}")
async def receive(user_id: int):
    user = users[user_id]
    return {"user": user}


@app.post("/users/")
async def create(user: User):
    users.append(user)
    return user


@app.put("/users/{user_id}")
async def updating(user_id: int, user: User):
    users[user_id] = user
    return {"user_id": user_id, "user": user}


@app.delete("/users/{user_id}")
async def delete_data(user_id: int):
    users.pop(user_id)
    return {"user_id": user_id}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
