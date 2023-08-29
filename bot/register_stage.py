import logging
from stage import Stage

from register_overwrite_init_stage import RegisterOverwriteInitSubstage

from overwrite.start import OverwriteStartStage


from get_id import get_id
from matching.stage import MatchStage

from stage_order import next_stage
from db.user import User
from db.match import get_user_by_telegram_id

from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram import F, Router

from sqlalchemy import select


class RegisterStage(Stage):
    state = State()
    name: str = "register"

    @staticmethod
    async def notify_waiting_pool_on_new_user(state: FSMContext, new_user: User) -> None:
        stmt = (
            select(User.id)
            .where(User.in_waiting_pool==True)
            .where(User.id!=new_user.id)
            # .where(new_user.is_eligible_candidate_for(User))
        )

        async with Stage.async_session() as session:
            target_ids = (await session.scalars(stmt)).all()

        for user_id in target_ids:
            async with Stage.async_session() as session:
                user = await get_user_by_telegram_id(telegram_id=user_id, session=session)

                if not user.in_waiting_pool:
                    logging.debug(
                        "%s was already notified, so there is no need to notify him again", user.id)
                    continue

                user.in_waiting_pool = False
                await session.commit()

                await MatchStage.get_next_match(
                    state,
                    user.id,
                    do_nothing_on_not_found=True,
                    # new_user,
                )

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
        await RegisterStage.notify_waiting_pool_on_new_user(state, user)

    @staticmethod
    def register(router: Router) -> None:
        RegisterOverwriteInitSubstage.register(router)
