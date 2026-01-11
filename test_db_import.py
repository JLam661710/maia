
from utils.db_client import db_client

def test_connection():
    print("Testing db_client import connection...")
    if db_client.client:
        print("✅ Success: db_client connected successfully.")
    else:
        print("❌ Fail: db_client failed to connect.")

if __name__ == "__main__":
    test_connection()
