import security

# The password Edna will use to log in
plain_password = "password123"

# Generate the secure bcrypt hash
hashed_password = security.get_password_hash(plain_password)

print("-------------------------------------------------")
print(f"Email: edna@springfield.edu")
print(f"Plain Password: {plain_password}")
print(f"Hashed Password: {hashed_password}")
print("-------------------------------------------------")