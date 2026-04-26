"""Script utilitas untuk menghapus webhook Telegram dan membersihkan pending updates."""

import asyncio

from telegram import Bot

from src.config import TELEGRAM_TOKEN


async def reset() -> None:
    """Hapus webhook dan bersihkan pending updates dari bot Telegram."""
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    print("Webhook dihapus, pending updates dibersihkan.")
    await bot.close()


if __name__ == "__main__":
    asyncio.run(reset())

