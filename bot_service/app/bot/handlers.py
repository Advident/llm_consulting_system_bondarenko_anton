from app.tasks.llm_tasks import llm_request
from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Приветственное сообщение."""
    await message.answer(
        "Привет! Сначала получи JWT в Auth Service, "
        "а потом отправь его командой:\n"
        "/token <your_jwt>"
    )


@router.message(Command("token"))
async def cmd_token(message: Message, command: CommandObject) -> None:
    """Сохраняет JWT пользователя после валидации."""
    if message.from_user is None:
        await message.answer("Не удалось определить пользователя Telegram.")
        return

    token = command.args
    if not token:
        await message.answer("Использование: /token <jwt>")
        return

    try:
        decode_and_validate(token)
    except ValueError as exc:
        await message.answer(f"Токен отклонён: {exc}")
        return

    redis_client = get_redis()
    key = f"token:{message.from_user.id}"
    await redis_client.set(key, token)

    await message.answer("Токен принят и сохранён.")


@router.message(F.text)
async def handle_text(message: Message) -> None:
    """Обрабатывает обычный текст пользователя."""
    if message.from_user is None:
        await message.answer("Не удалось определить пользователя Telegram.")
        return

    redis_client = get_redis()
    key = f"token:{message.from_user.id}"
    token = await redis_client.get(key)

    if not token:
        await message.answer(
            "Токен не найден. Сначала авторизуйтесь в Auth Service "
            "и отправьте команду /token <jwt>."
        )
        return

    try:
        payload = decode_and_validate(token)
    except ValueError as exc:
        await message.answer(
            f"Сохранённый токен недействителен: {exc}\n"
            "Отправьте новый токен через /token <jwt>."
        )
        return

    llm_request.delay(message.chat.id, message.text)

    await message.answer(
        f"Запрос принят в обработку. JWT валиден, user_id={payload['sub']}."
    )