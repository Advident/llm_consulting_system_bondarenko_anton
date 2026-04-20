import asyncio

from aiogram import Bot

from app.core.config import settings
from app.infra.celery_app import celery_app
from app.services.openrouter_client import OpenRouterClient


async def _process_llm_request(tg_chat_id: int, prompt: str) -> None:
    """Асинхронная логика обработки LLM-запроса."""
    client = OpenRouterClient()
    answer = await client.ask(prompt)

    bot = Bot(token=settings.telegram_bot_token)
    try:
        await bot.send_message(chat_id=tg_chat_id, text=answer)
    finally:
        await bot.session.close()


@celery_app.task(name="app.tasks.llm_tasks.llm_request")
def llm_request(tg_chat_id: int, prompt: str) -> str:
    """Celery-задача: вызывает LLM и отправляет ответ пользователю."""
    asyncio.run(_process_llm_request(tg_chat_id, prompt))
    return "ok"