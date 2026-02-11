import sys
import os
from fastapi.testclient import TestClient

# Add project root to path
sys.path.append(os.getcwd())

from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Student Wallet API"}
    print("Root endpoint verified.")

def test_routers_accessible():
    # Test a few endpoints to ensure routers are mounted
    v1 = settings.API_V1_STR
    
    # Parents
    response = client.get(f"{v1}/parents/")
    print(f"Parents index status: {response.status_code}")
    assert response.status_code in [200, 401, 403]
    
    # Students
    response = client.get(f"{v1}/students/")
    print(f"Students index status: {response.status_code}")
    assert response.status_code in [200, 401, 403]
    
    # Products
    response = client.get(f"{v1}/products/")
    print(f"Products index status: {response.status_code}")
    assert response.status_code in [200, 401, 403]

if __name__ == "__main__":
    try:
        test_read_root()
        test_routers_accessible()
        print("API Layer Verification Successful: All routers are correctly mounted.")
    except Exception as e:
        print(f"API Layer Verification Failed: {e}")
        sys.exit(1)
