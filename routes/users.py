from fastapi import APIRouter, HTTPException
from schema import User, UserCreate
from user_store import UserStore
from typing import List

router = APIRouter()
store = UserStore("users.txt")

DATA_FILE = "users.txt"

#endpoints

#create user
@router.post("/", response_model=User)
def create_user(user: UserCreate):
    users = store.load()

    if not users:
        next_id = 1
    else:
        next_id = max(u["id"] for u in users) + 1

    new_user = {"id": next_id, **user.model_dump()}
    users.append(new_user)

    store.save(users)
    return new_user

#get all users
@router.get("/", response_model=List[User])
def get_all_users():
    return store.load()

#search users
@router.get("/search", response_model=List[User])
def search_users(q: str):
    users = store.load()
    return [user for user in users if q.lower() in user["name"].lower()]

#get user by id
@router.post("/{user_id}", response_model=User)
def get_user(user_id: int):
    user = store.find_by_id(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

#update user
@router.put("/{user_id}", response_model=User)
def update_user(user_id, updated: UserCreate):
    success = store.update_user(user_id, updated.model_dump())
    if success:
        return store.find_by_id(user_id)
    raise HTTPException(status_code=404, detail="User not found")

#delete user
@router.delete("/{user_id}")
def delete_user(user_id):
    success = store.delete_user(user_id)
    if success:
        return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")