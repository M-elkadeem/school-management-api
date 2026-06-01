from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text

# Initialize the FastAPI app
app = FastAPI(title="School Management API")

# The connection string uses the exact credentials we set up earlier
DATABASE_URL = "postgresql://platform_user:my_secure_password@localhost/school_db"

# Create the database engine
engine = create_engine(DATABASE_URL)

@app.get("/")
def read_root():
    return {"message": "System Online. Welcome to the API."}

@app.get("/api/users")
def get_all_users():
    try:
        # Open a connection to the database
        with engine.connect() as connection:
            # Execute a raw SQL query
            result = connection.execute(text("SELECT id, name, email, role FROM users;"))
            
            # Format the results into a list of dictionaries
            users = [{"id": str(row.id), "name": row.name, "email": row.email, "role": row.role} for row in result]
            return {"status": "success", "data": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))