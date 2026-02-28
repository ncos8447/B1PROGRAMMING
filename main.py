from fastapi import FastAPI
from routes import users

app = FastAPI(
    title="User Management FastAPI App",
    description="FastAPI backend",
    version="1.0.0",
)

#user routes
app.include_router(users.router, prefix="/users", tags=["users"])

#root endpoint
@app.get("/")
def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/health")
def detailed_health_check():
    return {"status": "healthy", "message": "just started"}

