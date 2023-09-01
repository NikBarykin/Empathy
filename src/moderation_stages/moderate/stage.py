from logging import Logger

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from stage import Stage

from utils.logger import create_logger
from utils.restart_state import restart_state

from .filter import ModeratorFilter


class ModerateStage(Stage):
    name: str = "Moderation-stage"
    __logger: Logger = create_logger(name)

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        pass

    @staticmethod
    async def process(message: Message, state: FSMContext):
        user_id: int = message.from_user.id
        await restart_state(state=state, user_id=user_id)
        ModerateStage.__logger.info("%s started moderating", user_id)
        await message.answer("Ты успешно вошел в режим модератора")
        await ModerateStage.next_stage.prepare(state)

    @staticmethod
    async def register(router: Router) -> None:
        router.message.register(
            ModerateStage.process,
            ModeratorFilter(logger=ModerateStage.__logger)
        )
