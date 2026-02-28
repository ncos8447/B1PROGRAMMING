from fastapi import FastAPI, HTTPException
from schema import User, UserCreate
from user_store import UserStore

app = FastAPI(
    title="user management api",
    version="1.0.0"
)

# initialize sqlite store
store = UserStore("routes.db")

@app.get("/")
def root():
    return {"message": "api running with sqlite"}

@app.get("/routes", response_model=list[User])
def get_users():
    # return all routes
    return store.load()

@app.post("/routes", response_model=User)
def create_user(user: UserCreate):
    # create new user
    new_id = store.save(user.dict())

    return {
        "id": new_id,
        "name": user.name,
        "email": user.email
    }

@app.get("/routes/{user_id}", response_model=User)
def get_user(user_id: int):
    # get user by id
    user = store.find_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return user

@app.put("/routes/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: UserCreate):
    # update user
    success = store.update_user(user_id, updated_user.dict())

    if not success:
        raise HTTPException(status_code=404, detail="user not found")

    return {
        "id": user_id,
        "name": updated_user.name,
        "email": updated_user.email
    }

@app.delete("/routes/{user_id}")
def delete_user(user_id: int):
    # delete user
    success = store.delete_user(user_id)

    if not success:
        raise HTTPException(status_code=404, detail="user not found")
    return {"message": "user deleted successfully"}