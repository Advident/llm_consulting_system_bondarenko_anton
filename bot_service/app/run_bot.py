import asyncio

from aiogram.exceptions import TelegramNetworkError

from app.bot.dispatcher import bot, dp


async def main() -> None:
    print("BOT STARTED")

    while True:
        try:
            await dp.start_polling(bot)
        except TelegramNetworkError as error:
            print(f"Telegram network error: {error}")
            print("Retrying in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as error:
            print(f"Unexpected bot error: {error}")
            raise


if __name__ == "__main__":
    asyncio.run(main())