from typing import Callable, Generator

import pytest
from fastapi.testclient import TestClient
from pydantic import EmailStr
from requests.models import Response

from app.main import app
from app.schemas.users import CreateUserData, LoginUserData, Role

from .dependencies import get_random_user_name

RandomUserFunction = Callable[[], CreateUserData]
LoginFunction = Callable[[TestClient, LoginUserData], Response]
SignupFunction = Callable[[TestClient, CreateUserData], Response]
DeleteFunction = Callable[[TestClient, str], Response]


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as cli:
        yield cli


@pytest.fixture
def create_random_user() -> RandomUserFunction:
    def _create_random_user(role: Role = Role.GUEST) -> CreateUserData:
        """Creates a random SignupUser"""
        random_username = get_random_user_name()
        user = CreateUserData(
            name=random_username,
            email=EmailStr(f"{random_username}@example.com"),
            password="a-super-secret-password",
            role=role,
        )
        return user

    return _create_random_user


@pytest.fixture
def signup_user() -> SignupFunction:
    def _signup_user(cli: TestClient, user: CreateUserData) -> Response:
        response = cli.post(
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


@pytest.fixture
def login_user() -> LoginFunction:
    def _login_user(cli: TestClient, user: LoginUserData) -> Response:
        response = cli.post(
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


@pytest.fixture
def delete_user() -> DeleteFunction:
    def _delete_user(cli: TestClient, token: str) -> Response:
        response = cli.delete(
            "/users/me",
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
        return response

    return _delete_user


def test_my_test(client: TestClient):
    user = LoginUserData(email=EmailStr("pepe@example.com"), password="secret")
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
    print(response.status_code)
    assert response.status_code == 200


def test_login(
    client: TestClient,
    login_user: LoginFunction,
    username="pepe@example.com",
    password="secret",
) -> str:
    response = login_user(client, LoginUserData(email=EmailStr(username), password=password))
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]
    return response.json()["access_token"]


def test_me_unauthorized(client: TestClient):
    response = client.get("/users/me")
    assert response.status_code == 401


def test_me(
    client: TestClient, login_user: LoginFunction, user="pepe@example.com", password="secret"
):
    token = test_login(client, login_user, username=user, password=password)

    response = client.get(
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
    client: TestClient,
    create_random_user: RandomUserFunction,
    signup_user: SignupFunction,
    login_user: LoginFunction,
    delete_user: DeleteFunction,
):
    user: CreateUserData = create_random_user()

    signup_user(
        client,
        user,
    )

    token = test_login(client, login_user, username=user.email, password=user.password)

    delete_user(client, token)


def test_fail_create_existing_user(client: TestClient, signup_user: SignupFunction):
    s_user = CreateUserData(
        name="pepe",
        email=EmailStr("pepe@example.com"),
        role=Role.GUEST,
        password="super-secret",
    )

    response = signup_user(client, s_user)
    assert response.status_code == 400


def test_unauthenticated_cannot_get_all_users(client: TestClient):
    response = client.get("/users")
    assert response.status_code == 401


def test_unauthorized_cannot_get_all_users(
    client: TestClient,
    create_random_user: RandomUserFunction,
    signup_user: SignupFunction,
    login_user: LoginFunction,
    delete_user: DeleteFunction,
):
    user: CreateUserData = create_random_user()
    signup_user(client, user)
    token = test_login(client, login_user, username=user.email, password=user.password)

    response = client.get(
        "/users",
        headers={
            "Content-Type": "application/json",
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403
    delete_user(client, token)


def test_admin_can_get_all_users(client: TestClient, login_user: LoginFunction):
    token = test_login(client, login_user)
    response = client.get(
        "/users",
        headers={
            "Content-Type": "application/json",
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
