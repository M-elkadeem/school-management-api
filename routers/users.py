from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from database import engine

# Create a router specifically for user endpoints
router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/")
def get_all_users():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT id, name, email, role FROM users;"))
            users = [{"id": str(row.id), "name": row.name, "email": row.email, "role": row.role} for row in result]
            return {"status": "success", "data": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))