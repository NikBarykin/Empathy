from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.methods import SendMessage

from stage import Stage

from utils.id import get_id

from .number_of_users import count_users


class StatisticsStage(Stage):
    """Some statistics about bot's users"""
    name: str = "Статистика"
    __prepare_state = State("prepare_" + name)

    @staticmethod
    async def prepare(state: FSMContext):
        await state.set_state(StatisticsStage.__prepare_state)

        await Stage.bot(
            SendMessage(
                chat_id=await get_id(state),
                text=f"Кол-во пользователей {count_users()}",
            )
        )

        return await StatisticsStage.next_stage.prepare(state)

    @staticmethod
    def register(router: Router) -> None:
        """There is nothing to process"""
