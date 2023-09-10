"""Menu with bot commands that user sees in telegram"""
from aiogram import Bot
from aiogram.types import BotCommand

from user_stages.config import MENU_STAGES


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        commands=[
            BotCommand(command=command_stage.name, description=command_stage.description)
            for command_stage in MENU_STAGES
        ]
    )
