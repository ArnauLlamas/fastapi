"""User base Tests"""
from typing import Callable
import pytest

from fastapi import Response
from fastapi.testclient import TestClient

from app.schemas.users import LoginUser, SignupUser, Role
from app.main import app

from .dependencies import get_random_user_name

RandomUserFunction = Callable[[Role], SignupUser]
LoginFunction = Callable[[TestClient, LoginUser], Response]
SignupFunction = Callable[[TestClient, SignupUser], Response]
DeleteFunction = Callable[[TestClient, str], Response]


class TestUserBase:
    """Class to test the users API"""

    client = TestClient(app)

    # pylint: disable=missing-function-docstring
    @staticmethod
    @pytest.fixture
    def create_random_user() -> RandomUserFunction:
        def _create_random_user(role: Role = Role.GUEST) -> SignupUser:
            """Creates a random SignupUser"""
            random_username = get_random_user_name()
            user = SignupUser(
                name=random_username,
                email=f"{random_username}@example.com",
                password="a-super-secret-password",
                role=role,
            )
            return user

        return _create_random_user

    @staticmethod
    @pytest.fixture
    def signup_user() -> SignupFunction:
        def _signup_user(client: TestClient, user: SignupUser) -> Response:
            response = client.post(
                "/signup",
                headers={"Content-Type": "application/json", "accept": "application/json"},
                json={
                    "name": f"{user.name}",
                    "email": f"{user.email}",
                    "password": f"{user.password}",
                    "role": f"{user.role}",
                },
            )
            return response

        return _signup_user

    @staticmethod
    @pytest.fixture
    def login_user() -> LoginFunction:
        def _login_user(client: TestClient, user: LoginUser) -> Response:
            response = client.post(
                "/login",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "accept": "application/json",
                },
                data={
                    "grant_type": "",
                    "username": f"{user.email}",
                    "password": f"{user.password}",
                    "scope": "",
                    "client_id": "",
                    "client_secret": "",
                },
            )
            return response

        return _login_user

    @staticmethod
    @pytest.fixture
    def delete_user() -> DeleteFunction:
        def _delete_user(client: TestClient, token: str) -> Response:
            response = client.delete(
                "/users/me",
                headers={
                    "Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": f"Bearer {token}",
                },
            )
            return response

        return _delete_user


class TestUserMe(TestUserBase):
    """Test base of /users/me endpoint"""

    # pylint: disable=missing-function-docstring
    def test_login(
        self, login_user: LoginFunction, username="pepe@example.com", password="secret"
    ) -> str:
        response = login_user(self.client, LoginUser(email=username, password=password))
        assert response.status_code == 200
        assert response.json()["token_type"] == "bearer"
        assert response.json()["access_token"]
        return response.json()["access_token"]

    def test_me_unauthorized(self):
        response = self.client.get("/users/me")
        assert response.status_code == 401

    def test_me(self, login_user: LoginFunction, user="pepe@example.com", password="secret"):
        token = self.test_login(login_user, username=user, password=password)

        response = self.client.get(
            "/users/me",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
        assert response.status_code == 200
        assert response.json()["email"] == user

    def test_create_login_delete(
        self,
        create_random_user: RandomUserFunction,
        signup_user: SignupFunction,
        login_user: LoginFunction,
        delete_user: DeleteFunction,
    ):
        user: SignupUser = create_random_user()

        signup_user(
            self.client,
            user,
        )

        token = self.test_login(login_user, username=user.email, password=user.password)

        delete_user(self.client, token)

    def test_fail_create_existing_user(self, signup_user):
        s_user = SignupUser(
            name="pepe", email="pepe@example.com", role=Role.GUEST, password="super-secret"
        )

        response = signup_user(self.client, s_user)
        assert response.status_code == 400

    def test_unauthenticated_cannot_get_all_users(self):
        response = self.client.get("/users")
        assert response.status_code == 401

    def test_unauthorized_cannot_get_all_users(
        self,
        create_random_user: RandomUserFunction,
        signup_user: SignupFunction,
        login_user: LoginFunction,
        delete_user: DeleteFunction,
    ):
        user: SignupUser = create_random_user()
        signup_user(self.client, user)
        token = self.test_login(login_user, username=user.email, password=user.password)

        response = self.client.get(
            "/users",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

        assert response.status_code == 403
        delete_user(self.client, token)

    def test_admin_can_get_all_users(self, login_user: LoginFunction):
        token = self.test_login(login_user)
        response = self.client.get(
            "/users",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

        assert response.status_code == 200
