from typing import List

from fastapi import APIRouter, HTTPException
from schema import User, UserCreate
import json
import os

router = APIRouter()

DATA_FILE = "users.txt"

#helper func

def read_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError:
            return []

def write_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

def get_next_id(users):
    if not users:
        return 1
    return max(user["id"] for user in users)+1

#endpoints

#create user
@router.post("/", response_model=User)
def create_user(user: UserCreate):
    users = read_users()
    new_user = {"id": get_next_id(users), **user.model_dump()}
    users.append(new_user)
    write_users(users)
    return new_user

#get all users
@router.get("/", response_model=List[User])
def get_all_users():
    users = read_users()
    return read_users()

#search users
@router.get("/search", response_model=List[User])
def search_users(q: str):
    users = read_users()
    return [user for user in users if q.lower() in user["name"].lower()]

#get user by id
@router.post("/{id}", response_model=User)
def get_user(id: int):
    users = read_users()
    for user in users:
        if user["id"] == id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

#update user
@router.put("/{id}", response_model=User)
def update_user(id: int, updated: UserCreate):
    users = read_users()
    for user in users:
        if user["id"] == id:
            user["name"] = updated.name
            user["email"] = updated.email
            write_users(users)
            return user
    raise HTTPException(status_code=404, detail="User not found")

#delete user
@router.delete("/{id}", response_model=User)
def delete_user(id: int):
    users = read_users()
    for i, user in enumerate(users):
        if user["id"] == id:
            users.pop(i)
            write_users(users)
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")