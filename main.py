from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import users, classes, auth, enrollments, admin
import os

app = FastAPI(title="School Management API")

# 1. Create an 'uploads' folder dynamically if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# 2. Mount the folder so files can be accessed directly via URL
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Connect the modular routers
app.include_router(users.router)
app.include_router(classes.router)
app.include_router(auth.router)
app.include_router(enrollments.router)
app.include_router(admin.router)
@app.get("/")
def read_root():
    return {"message": "System Online. Modular architecture active."}

app.include_router(auth.router)