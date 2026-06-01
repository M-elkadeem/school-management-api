from sqlalchemy import create_engine

DATABASE_URL = "postgresql://platform_user:my_secure_password@localhost/school_db"

# Create and export the database engine
engine = create_engine(DATABASE_URL)