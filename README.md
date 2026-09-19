# 🏫 School Management API

A RESTful API built with FastAPI and PostgreSQL for managing school operations — authentication, role-based access, student enrollments, and file uploads.

## ✨ Features

- JWT authentication with role-based access control (Admin, Teacher, Student)
- Student-class enrollment management (many-to-many relations)
- File uploads for class materials
- Paginated endpoints for performance
- Full test coverage with Pytest

## 🛠️ Tech Stack

FastAPI · PostgreSQL · SQLAlchemy · Uvicorn · JWT (Python-Jose) · Bcrypt (Passlib) · Pytest

## 🚀 Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

**2. Set up a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up the database**

Create a PostgreSQL database, then run:
```bash
psql -U your_username -d school_db -f db/init.sql
```

**5. Run the server**
```bash
uvicorn main:app --reload
```

## 📖 API Docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Tests

```bash
pytest -v
```