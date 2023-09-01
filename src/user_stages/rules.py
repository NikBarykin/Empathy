from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from stage import Stage

from utils.id import get_id


RULES: str = """Правила:
1. Запрещена любая нецензурная речь
2. Ты должен присутствовать на фотографии
3. Должно быть понятно, кто из людей на фотографии является тобой
"""


class RulesStage(Stage):
    name: str = "rules"
    description: str = "Правила"

    @staticmethod
    async def prepare(state: FSMContext):
        pass

    @staticmethod
    async def process(_: Message, state: FSMContext):
        return Stage.bot.send_message(
            chat_id=await get_id(state),
            text=RULES,
        )

    @staticmethod
    def register(router: Router):
        router.message.register(
            RulesStage.prepare,
            Command(RulesStage.name),
        )