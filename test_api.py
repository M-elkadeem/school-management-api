from fastapi.testclient import TestClient
from main import app

# Create a test client that simulates a web browser talking to your API
client = TestClient(app)

def test_read_root():
    """Test that the API is online and the main router is working."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "System Online. Modular architecture active."}

def test_get_all_users():
    """Test that the users endpoint successfully fetches data from PostgreSQL."""
    response = client.get("/api/users")
    
    # Check that the request was successful
    assert response.status_code == 200
    
    # Check that the response contains the 'status' and 'data' keys we designed
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    
    # Verify that we actually got users back (Principal Skinner and Edna)
    assert len(data["data"]) > 0
    
    # Verify the structure of a user object
    first_user = data["data"][0]
    assert "id" in first_user
    assert "name" in first_user
    assert "role" in first_user

def test_upload_attachment():
    """Test that a teacher can successfully upload a syllabus file."""
    
    # 1. Fetch an existing announcement to get a valid ID to attach the file to
    # (Using the Biology class ID we verified earlier)
    res = client.get("/api/classes/a640a909-525d-4f14-a4ee-46dc625c620a/announcements")
    
    # Ensure there is at least one announcement to attach to
    announcements = res.json().get("data", [])
    assert len(announcements) > 0
    announcement_id = announcements[0]["id"]
    
    # 2. Simulate a PDF file upload in memory
    # The format is: {"field_name": ("filename", b"byte_content", "mime_type")}
    dummy_file = {"file": ("test_syllabus.pdf", b"Fake PDF file contents", "application/pdf")}
    
    # 3. Fire the POST request
    response = client.post(f"/api/announcements/{announcement_id}/attachments", files=dummy_file)
    
    # 4. Verify the database and server accepted it
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "file_url" in data
    assert data["file_url"].endswith(".pdf")