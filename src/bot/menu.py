"""Menu with bot commands that user sees in telegram"""
from aiogram import Bot
from aiogram.types import BotCommand

from user_stages.profile import ProfileStage
from user_stages.start import StartStage
from user_stages.rules import RulesStage


COMMAND_STAGES = (
    StartStage, ProfileStage, RulesStage)


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        commands=[
            BotCommand(command=command_stage.name, description=command_stage.description)
            for command_stage in COMMAND_STAGES
        ]
    )
