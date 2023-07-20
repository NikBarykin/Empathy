from .base import BaseStage
from .personal_interests import PersonalInterestsStage

from aiogram import Router, types
from aiogram.types import InlineKeyboardButton
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Text


class PreferredInterestsStage(BaseStage):
    state = State()
    name: str = "предпочитаемые интересы"
    question_text: str = "Предпочитаемые интересы партнера"
    submit_text: str = "Отмеченные предпочитаемые интересы партнера"

    @staticmethod
    async def get_kb_builder(_, state: FSMContext) -> InlineKeyboardBuilder:
        result: InlineKeyboardBuilder = await BaseStage.get_kb_builder(PreferredInterestsStage, state)
        result.row(
            InlineKeyboardButton(
                text="подтвердить такие же интересы, как у меня",
                callback_data="submit_interests_same",
            )
        )
        return result

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        await BaseStage.prepare_base(PreferredInterestsStage, state)

    @staticmethod
    async def process_callback_check_interest(
        callback: types.CallbackQuery,
        state: FSMContext,
    ) -> None:
        await BaseStage.process_callback_check_interest(
            PreferredInterestsStage, callback, state)

    @staticmethod
    async def process_callback_go_page(
        callback: types.CallbackQuery,
        state: FSMContext,
    ) -> None:
        await BaseStage.process_callback_go_page(
            PreferredInterestsStage, callback, state)

    @staticmethod
    async def process_callback_submit(
        callback: types.CallbackQuery,
        state: FSMContext,
    ) -> None:
        await BaseStage.process_callback_submit(
            PreferredInterestsStage, callback, state)

    @staticmethod
    async def process_callback_submit_same(
        callback: types.CallbackQuery,
        state: FSMContext,
    ):
        personal_interests = await BaseStage.get_interests(
            PersonalInterestsStage, state)

        await state.update_data(
            **{PreferredInterestsStage.name: personal_interests})

        await PreferredInterestsStage.process_callback_submit(
            callback, state)

    @staticmethod
    def register(router: Router) -> None:
        BaseStage.register_base(PreferredInterestsStage, router)

        router.callback_query.register(
            PreferredInterestsStage.process_callback_submit_same,
            Text("submit_interests_same"),
            PreferredInterestsStage.state,
        )
