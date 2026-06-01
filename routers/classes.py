from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import text
from database import engine
from schemas import AnnouncementCreate
from security import SECRET_KEY, ALGORITHM
import shutil
import uuid

router = APIRouter(prefix="/api", tags=["Classes & Announcements"])

# This tells FastAPI where to look for the token when a route is protected
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# A helper function to verify the token and extract the user's ID
def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
            
        # Role-Based Access Control: Only Teachers and Admins can proceed
        if role != "TEACHER" and role != "ADMIN":
            raise HTTPException(status_code=403, detail="Only teachers can post announcements")
            
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


@router.post("/announcements")
def create_announcement(announcement: AnnouncementCreate, current_user_id: str = Depends(get_current_user_id)):
    try:
        with engine.connect() as connection:
            query = text("""
                INSERT INTO announcements (class_id, author_id, title, content)
                VALUES (:class_id, :author_id, :title, :content)
                RETURNING id;
            """)
            
            # We map 'author_id' directly to the securely extracted 'current_user_id'
            result = connection.execute(query, {
                "class_id": announcement.class_id,
                "author_id": current_user_id,
                "title": announcement.title,
                "content": announcement.content
            })
            
            connection.commit() 
            new_id = result.fetchone()[0]
            
            return {"status": "success", "message": "Announcement posted!", "id": str(new_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# We add 'skip' and 'limit' with default values of 0 and 10
@router.get("/classes/{class_id}/announcements")
def get_class_announcements(class_id: str, skip: int = 0, limit: int = 10):
    try:
        with engine.connect() as connection:
            # We add LIMIT and OFFSET to the SQL query
            query = text("""
                SELECT a.id, a.title, a.content, a.created_at, u.name as author_name
                FROM announcements a
                JOIN users u ON a.author_id = u.id
                WHERE a.class_id = :class_id
                ORDER BY a.created_at DESC
                LIMIT :limit OFFSET :skip;
            """)
            
            # Pass the new parameters into the execution
            result = connection.execute(query, {
                "class_id": class_id, 
                "limit": limit, 
                "skip": skip
            })
            
            announcements = [
                {
                    "id": str(row.id),
                    "title": row.title,
                    "content": row.content,
                    "author": row.author_name,
                    "date": row.created_at.strftime("%Y-%m-%d %H:%M")
                }
                for row in result
            ]
            return {"status": "success", "data": announcements, "showing": len(announcements)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/announcements/{announcement_id}/attachments")
def upload_attachment(announcement_id: str, file: UploadFile = File(...)):
    try:
        # 1. Generate a unique filename to prevent overwriting
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = f"uploads/{unique_filename}"
        
        # 2. Save the physical file locally to the 'uploads' folder
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 3. Save the record in the PostgreSQL database
        file_url = f"/uploads/{unique_filename}"
        
        with engine.connect() as connection:
            query = text("""
                INSERT INTO attachments (announcement_id, file_url, file_type)
                VALUES (:announcement_id, :file_url, :file_type)
                RETURNING id;
            """)
            
            result = connection.execute(query, {
                "announcement_id": announcement_id,
                "file_url": file_url,
                "file_type": file.content_type
            })
            
            connection.commit()
            attachment_id = result.fetchone()[0]
            
        return {
            "status": "success", 
            "message": "File attached successfully!", 
            "attachment_id": str(attachment_id),
            "file_url": file_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))