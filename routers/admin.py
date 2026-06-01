from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import text
from database import engine
from security import SECRET_KEY, ALGORITHM
from pydantic import BaseModel

router = APIRouter(prefix="/api/admin", tags=["Admin & Management"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# The RBAC Bouncer: This checks the token specifically for the "ADMIN" role
def require_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get("role")
        
        # If they are a STUDENT or TEACHER, kick them out
        if role != "ADMIN":
            raise HTTPException(status_code=403, detail="Access Denied: Super Admin privileges required.")
            
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


class ClassCreate(BaseModel):
    name: str
    description: str
# 1. Add teacher_id to the expected JSON body
class ClassCreate(BaseModel):
    name: str
    description: str
    teacher_id: str

# Protected Admin Route: Create a new class
@router.post("/classes")
def create_new_class(class_data: ClassCreate, admin_id: str = Depends(require_admin)):
    try:
        with engine.connect() as connection:
            # 2. Add teacher_id to the INSERT statement
            query = text("""
                INSERT INTO classes (name, description, teacher_id)
                VALUES (:name, :description, :teacher_id)
                RETURNING id;
            """)
            
            # 3. Pass the teacher_id to the database
            result = connection.execute(query, {
                "name": class_data.name,
                "description": class_data.description,
                "teacher_id": class_data.teacher_id
            })
            
            connection.commit() 
            new_id = result.fetchone()[0]
            
            return {"status": "success", "message": "New class created successfully!", "class_id": str(new_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))