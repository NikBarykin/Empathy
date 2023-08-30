from aiogram import Bot

from stage import Stage

from .config import TOKEN
from .menu import set_commands


async def setup_bot() -> Bot:
    """Create and setup bot"""
    bot = Bot(token=TOKEN)
    Stage.bot = bot
    await set_commands(bot)
    # skip messages
    await bot.delete_webhook(drop_pending_updates=True)

    return bot
