"""
Profile stage

When you want to send someone your profile or update/complete you profile
"""
from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from database.user import User

from stage import Stage, go_stage

from engine.user import get_user_by_id

from utils.keyboard import send_reply_kb
from utils.id import get_id
from utils.prev_stage import PREV_STAGE_KB, make_prev_stage_processor, PREV_STAGE_FILTER

from user_stages.choose_update import ChooseUpdateStage
from user_stages.freeze import FreezeStage

from .send import send_profile
from .keyboard import QUERY_KB
from .callback_factory import GoFreezeCallbackFactory, GoUpdateCallbackFactory

class ProfileStage(Stage):
    """User's profile stage"""
    name: str = "my_profile"
    description: str = "Моя анкета"
    __main_state = State(state="main_" + name)
    __prepare_state = State(state="prepare_" + name)

    @staticmethod
    async def prepare(state: FSMContext):
        await state.set_state(ProfileStage.__prepare_state)

        # TODO: delete last match-message

        user: User = await get_user_by_id(await get_id(state))

        await send_reply_kb(chat_id=user.id, kb=PREV_STAGE_KB)

        await send_profile(
            chat_id=user.id,
            user=user,
            reply_markup=QUERY_KB,
        )

        await state.set_state(ProfileStage.__main_state)

    @staticmethod
    async def process_update(callback: CallbackQuery, state: FSMContext):
        result = await go_stage(
            departure=ProfileStage,
            destination=ChooseUpdateStage,
            state=state,
        )
        await callback.answer()
        return result

    @staticmethod
    async def process_freeze(callback: CallbackQuery, state: FSMContext):
        result = await go_stage(
            departure=ProfileStage,
            destination=FreezeStage,
            state=state,
        )
        await callback.answer()
        return result

    @staticmethod
    def register(router: Router) -> None:
        if ProfileStage.prev_stage is not None:
            router.message.register(
                make_prev_stage_processor(ProfileStage),
                ProfileStage.__main_state,
                PREV_STAGE_FILTER,
            )

        router.callback_query.register(
            ProfileStage.process_update,
            ProfileStage.__main_state,
            GoUpdateCallbackFactory.filter(),
        )

        router.callback_query.register(
            ProfileStage.process_freeze,
            ProfileStage.__main_state,
            GoFreezeCallbackFactory.filter(),
        )
