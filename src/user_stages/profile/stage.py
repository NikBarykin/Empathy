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

from utils.keyboard import send_reply_kb, RowKeyboard
from utils.id import get_id
from utils.prev_stage import PREV_STAGE_KB, make_prev_stage_processor, PREV_STAGE_FILTER
from utils.order import make_stage_jumper

from user_stages.choose_update import ChooseUpdateStage
from user_stages.freeze import FreezeStage

from .send import send_profile
from .keyboard import QUERY_KB
from .callback_factory import GoFreezeCallbackFactory, GoUpdateCallbackFactory
from .constants import CONTINUE_TEXT


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

        if ProfileStage.next_stage is not None:
            await send_reply_kb(chat_id=user.id, kb=RowKeyboard(CONTINUE_TEXT))

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
        if ProfileStage.next_stage is not None:
            router.message.register(
                make_stage_jumper(target_stage=ProfileStage.next_stage),
                ProfileStage.__main_state,
                F.text==CONTINUE_TEXT,
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
