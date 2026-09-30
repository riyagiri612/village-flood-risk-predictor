from users import register_user, verify_user, init_users_file
import os

# Start completely fresh for this test
if os.path.exists("users.csv"):
    os.remove("users.csv")

init_users_file()

# Try registering a test user
success = register_user("Test User", "test@example.com", "password123")
print(f"Registration success: {success}")

# Try verifying with the exact same credentials
result = verify_user("test@example.com", "password123")
print(f"Login result: {result}")

# Try verifying with wrong password, to confirm it correctly fails
wrong_result = verify_user("test@example.com", "wrongpassword")
print(f"Wrong password result (should be None): {wrong_result}")