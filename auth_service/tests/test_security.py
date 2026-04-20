from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_password_hashing():
    password = "secret123"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)


def test_jwt_creation_and_decode():
    token = create_access_token(user_id=1, role="user")

    payload = decode_token(token)

    assert payload["sub"] == "1"
    assert payload["role"] == "user"
    assert "iat" in payload
    assert "exp" in payload