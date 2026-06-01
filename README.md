# 🏫 School Management API

A robust, modular, and fully-tested RESTful API built with **FastAPI** and **PostgreSQL**. This backend engine manages school operations, handling everything from user authentication and role-based access control to relational student enrollments and secure file uploads.

---

## ✨ Core Features

* **Modular Architecture:** Cleanly separated endpoints using FastAPI Routers (`Auth`, `Admin`, `Classes`, `Enrollments`, `Users`).

* **Advanced Security:**

  * Password hashing via `bcrypt`
  * Secure endpoints protected by **JWT (JSON Web Tokens)**
  * **Role-Based Access Control (RBAC):** Strict permissions separating `ADMIN`, `TEACHER`, and `STUDENT` capabilities

* **Relational Data Management:** Seamless handling of Many-to-Many relationships (e.g., enrolling students into classes) using SQLAlchemy and PostgreSQL.

* **File Handling:** Built-in endpoints for teachers to upload physical files (like PDF syllabuses) and link them to class announcements.

* **Performance:** Implemented query parameters for data pagination to ensure high performance at scale.

* **Automated Testing:** Fully tested routes using `pytest` and `httpx`.

---

## 🛠️ Tech Stack

* **Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Server:** Uvicorn
* **Authentication:** Python-Jose (JWT), Passlib (Bcrypt)
* **Testing:** Pytest

---

## 🚀 Getting Started (Local Development)

Follow these instructions to get a copy of the project up and running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/AhmedKhalifa3/school-management-api.git
cd school-management-api
```

### 2. Set Up the Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows use:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Ensure you have PostgreSQL running locally.

First, create a new empty database (e.g., `school_db`).

Then, initialize the database schema using the provided SQL blueprint. You can do this via the command line:

```bash
psql -U your_username -d school_db -f db/init.sql
```

Alternatively, you can open the `db/init.sql` file and run it directly inside a GUI tool like DBeaver or pgAdmin.

### 5. Run the Server

Start the Uvicorn server with hot-reloading enabled:

```bash
uvicorn main:app --reload
```

---

## 📖 API Documentation

Once the server is running, FastAPI automatically generates beautiful, interactive API documentation.

You can explore all endpoints, test data, and log in directly from your browser:

* **Swagger UI:** `http://localhost:8000/docs`
* **ReDoc:** `http://localhost:8000/redoc`

---

## 🧪 Running Tests

To verify the integrity of the API, run the automated test suite:

```bash
pytest -v
```
