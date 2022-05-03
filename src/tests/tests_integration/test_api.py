from fastapi.testclient import TestClient

from app.main import app


class TestAPI:
    """Base class to instantiate the client and test the API configuration"""

    client = TestClient(app)

    def test_status(self):
        response = self.client.get("/status")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}
