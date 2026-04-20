from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest
from jose import jwt

from app.bot import handlers
from app.core.config import settings


def create_test_token(
    sub: str = "1",
    role: str = "user",
    expires_delta_minutes: int = 60,
) -> str:
    """Создаёт валидный тестовый JWT."""
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=expires_delta_minutes)

    payload = {
        "sub": sub,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )


class FakeMessage:
    """Простая заглушка aiogram Message для тестов."""

    def __init__(self, text: str, user_id: int = 1001, chat_id: int = 2001):
        self.text = text
        self.from_user = SimpleNamespace(id=user_id)
        self.chat = SimpleNamespace(id=chat_id)
        self.answers: list[str] = []

    async def answer(self, text: str) -> None:
        self.answers.append(text)


@pytest.mark.asyncio
async def test_cmd_token_saves_token(fake_redis, mocker):
    token = create_test_token(sub="42")
    message = FakeMessage(text=f"/token {token}", user_id=111)

    mocker.patch("app.bot.handlers.get_redis", return_value=fake_redis)
    command = SimpleNamespace(args=token)

    await handlers.cmd_token(message, command)

    saved = await fake_redis.get("token:111")

    assert saved == token
    assert message.answers == ["Токен принят и сохранён."]


@pytest.mark.asyncio
async def test_cmd_token_without_args(fake_redis, mocker):
    message = FakeMessage(text="/token", user_id=111)

    mocker.patch("app.bot.handlers.get_redis", return_value=fake_redis)
    command = SimpleNamespace(args=None)

    await handlers.cmd_token(message, command)

    assert message.answers == ["Использование: /token <jwt>"]


@pytest.mark.asyncio
async def test_handle_text_without_saved_token(fake_redis, mocker):
    message = FakeMessage(text="Привет", user_id=222)

    mocker.patch("app.bot.handlers.get_redis", return_value=fake_redis)
    delay_mock = mocker.patch("app.bot.handlers.llm_request.delay")

    await handlers.handle_text(message)

    delay_mock.assert_not_called()
    assert len(message.answers) == 1
    assert "Токен не найден" in message.answers[0]


@pytest.mark.asyncio
async def test_handle_text_with_saved_token_calls_celery(fake_redis, mocker):
    token = create_test_token(sub="77")
    await fake_redis.set("token:333", token)

    message = FakeMessage(text="Расскажи про JWT", user_id=333, chat_id=444)

    mocker.patch("app.bot.handlers.get_redis", return_value=fake_redis)
    delay_mock = mocker.patch("app.bot.handlers.llm_request.delay")

    await handlers.handle_text(message)

    delay_mock.assert_called_once_with(444, "Расскажи про JWT")
    assert len(message.answers) == 1
    assert "Запрос принят" in message.answers[0]


@pytest.mark.asyncio
async def test_handle_text_with_invalid_saved_token(fake_redis, mocker):
    await fake_redis.set("token:555", "bad-token-value")
    message = FakeMessage(text="Привет", user_id=555)

    mocker.patch("app.bot.handlers.get_redis", return_value=fake_redis)
    delay_mock = mocker.patch("app.bot.handlers.llm_request.delay")

    await handlers.handle_text(message)

    delay_mock.assert_not_called()
    assert len(message.answers) == 1
    assert "Сохранённый токен недействителен" in message.answers[0]