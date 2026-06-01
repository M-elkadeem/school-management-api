from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import text
from database import engine
from pydantic import BaseModel
from security import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/api", tags=["Enrollments"])

# We define a more permissive bouncer here. 
# Students need to be able to fetch their own classes, so we don't restrict this to just TEACHERs.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_logged_in_user_id(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
            
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# Define the expected JSON body for enrolling a student
class EnrollmentCreate(BaseModel):
    student_id: str

# 1. Endpoint to enroll a student into a class
@router.post("/classes/{class_id}/enroll")
def enroll_student(class_id: str, enrollment: EnrollmentCreate, current_user_id: str = Depends(get_logged_in_user_id)):
    try:
        with engine.connect() as connection:
            # We use ON CONFLICT DO NOTHING to prevent errors if a student is enrolled twice
            query = text("""
                INSERT INTO enrollments (user_id, class_id)
                VALUES (:user_id, :class_id)
                ON CONFLICT (user_id, class_id) DO NOTHING;
            """)
            
            connection.execute(query, {
                "user_id": enrollment.student_id,
                "class_id": class_id
            })
            
            connection.commit() 
            
            return {"status": "success", "message": "Student successfully enrolled!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Endpoint for a user to see ONLY the classes they are enrolled in
@router.get("/users/me/classes")
def get_my_classes(current_user_id: str = Depends(get_logged_in_user_id)):
    try:
        with engine.connect() as connection:
            # We use a JOIN to cross-reference the enrollments table with the classes table
            query = text("""
                SELECT c.id, c.name, c.description
                FROM classes c
                JOIN enrollments e ON c.id = e.class_id
                WHERE e.user_id = :current_user_id;
            """)
            
            result = connection.execute(query, {"current_user_id": current_user_id})
            
            classes = [
                {
                    "id": str(row.id),
                    "name": row.name,
                    "description": row.description
                }
                for row in result
            ]
            
            return {"status": "success", "data": classes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))