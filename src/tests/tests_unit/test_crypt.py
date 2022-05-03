import random
import string

import pytest

from app.libs.crypt import crypt


@pytest.fixture
def password() -> str:
    return "".join(
        random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(12)
    )


def test_hash_password(password):
    hashed_password = crypt.hash_password(password)
    assert hashed_password != password


def test_verify_password(password):
    hashed_password = crypt.hash_password(password)
    assert crypt.verify_password(password, hashed_password)
