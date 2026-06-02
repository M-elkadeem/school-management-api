from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import text
from database import engine

# Assuming you have a security.py file with your hashing function!
from security import get_password_hash 

router = APIRouter(prefix="/api/public", tags=["Public Registration"])

# The expected JSON payload from the frontend
class SchoolRegistration(BaseModel):
    school_name: str
    address: str
    admin_name: str
    admin_email: EmailStr
    admin_password: str

@router.post("/register-school")
def register_new_school(payload: SchoolRegistration):
    try:
        # engine.begin() automatically opens a transaction.
        # If ANY error happens inside this block, it instantly rolls back BOTH queries.
        with engine.begin() as connection:
            
            # Step 1: Create the School
            school_query = text("""
                INSERT INTO schools (name, address)
                VALUES (:name, :address)
                RETURNING id;
            """)
            school_result = connection.execute(school_query, {
                "name": payload.school_name,
                "address": payload.address
            })
            new_school_id = school_result.fetchone()[0]

            # Step 2: Create the Admin User for that School
            hashed_pw = get_password_hash(payload.admin_password)
            user_query = text("""
                INSERT INTO users (school_id, name, email, password_hash, role)
                VALUES (:school_id, :name, :email, :password_hash, 'ADMIN')
                RETURNING id;
            """)
            user_result = connection.execute(user_query, {
                "school_id": new_school_id,
                "name": payload.admin_name,
                "email": payload.admin_email,
                "password_hash": hashed_pw
            })
            new_admin_id = user_result.fetchone()[0]

            return {
                "status": "success", 
                "message": "School and Admin account created successfully!",
                "school_id": str(new_school_id),
                "admin_id": str(new_admin_id)
            }
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")