from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import users, classes, auth, enrollments, admin, registration
import os
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="School Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # This is Vite's default port
    allow_credentials=True,
    allow_methods=["*"], # Allows POST, GET, PUT, DELETE, etc.
    allow_headers=["*"], # Allows all headers
)

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
app.include_router(registration.router)
@app.get("/")
def read_root():
    return {"message": "System Online. Modular architecture active."}

app.include_router(auth.router)