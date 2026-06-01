from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text
from database import engine
import security

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with engine.connect() as connection:
        # Find the user by email
        query = text("SELECT id, email, password_hash, role FROM users WHERE email = :email")
        result = connection.execute(query, {"email": form_data.username}).fetchone()
        
        # Check if user exists and password matches
        # Note: Because our seed data used fake hashes, this will only work with newly created users
        # who have properly hashed passwords.
        if not result or not security.verify_password(form_data.password, result.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Mint the token, storing their ID and Role inside it
        access_token = security.create_access_token(
            data={"sub": str(result.id), "role": result.role}
        )
        
        return {"access_token": access_token, "token_type": "bearer"}