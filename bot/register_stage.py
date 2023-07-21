import logging
from stage import Stage

from register_overwrite_init_stage import RegisterOverwriteInitSubstage

from overwrite.start import OverwriteStartStage


from command_start import get_id
from matching.stage import MatchStage

from stage_order import next_stage
from db.user import User

from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram import F, Router

from sqlalchemy import select


class RegisterStage(Stage):
    state = State()
    name: str = "register"

    @staticmethod
    async def notify_waiting_pool_on_new_user(new_user: User) -> None:
        stmt = (
            select(User)
            .where(User.in_waiting_pool==True)
            # .where(new_user.is_eligible_candidate_for(User))
        )

        async with Stage.async_session() as session:
            async with session.begin():
                for user in (await session.scalars(stmt)).all():
                    logging.debug(f"{user.name} was notified""")
                    await MatchStage.get_next_match(
                        user.id,
                        do_nothing_on_not_found=True,
                        # new_user,
                    )
                    user.in_waiting_pool = False

    @staticmethod
    async def create_and_insert_user(state: FSMContext) -> None:
        user: User = User.from_fsm_data(await state.get_data())
        await user.insert_to(Stage.async_session)

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        user: User = User.from_fsm_data(await state.get_data())
        await user.insert_to(Stage.async_session)

        await RegisterOverwriteInitSubstage.prepare(state)

        await next_stage(RegisterStage, state)
        await RegisterStage.notify_waiting_pool_on_new_user(user)

    @staticmethod
    def register(router: Router) -> None:
        RegisterOverwriteInitSubstage.register(router)
