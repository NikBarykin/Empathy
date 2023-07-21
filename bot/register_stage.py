from stage import Stage
from command_start import get_id
from matching.stage import MatchStage

from stage_order import next_stage
from db.user import User
import logging

from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext

from sqlalchemy import select


class RegisterStage(Stage):
    state = State()
    name: str = "register"

    @staticmethod
    async def notify_waiting_pool() -> None:
        stmt = select(User).where(User.in_waiting_pool==True)
        async with Stage.async_session() as session:
            async with session.begin():
                for user in (await session.scalars(stmt)).all():
                    logging.debug(f"{user.name} was notified""")
                    await MatchStage.get_next_match(
                        user.telegram_id,
                    )
                    user.in_waiting_pool = False

    @staticmethod
    async def create_and_insert_user(state: FSMContext) -> None:
        user: User = User.from_fsm_data(await state.get_data())
        await user.insert_to(Stage.async_session)

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        await RegisterStage.create_and_insert_user(state)
        await next_stage(RegisterStage, state)
        await RegisterStage.notify_waiting_pool()

    @staticmethod
    def register(*args, **kwargs) -> None:
        pass
