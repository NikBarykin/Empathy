from __future__ import annotations
from dummy_callback_factory import DummyCallbackFactory
from get_id import get_id
from stage import Stage, StageType
from constants import INTEREST_PAGES, CHECK_MARK_EMOJI

from aiogram import types, Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from constants import NO_INTERESTS, NO_INTEREST_PAGES

from typing import Set, Type, Dict, Iterable

from stage_order import next_stage
from dummy_callback_factory import DummyCallbackFactory


class BaseStage(Stage):
    # TODO: move page logic to other class
    @staticmethod
    async def get_page_i(state: FSMContext) -> int:
        return (await state.get_data())['interest_page_i']

    @staticmethod
    async def set_page_i(state: FSMContext, new_value: int) -> None:
        await state.update_data(**{'interest_page_i': new_value})

    @staticmethod
    async def get_interests(
        stage: Type[BaseStage],
        state: FSMContext,
    ) -> Set[str]:
        return (await state.get_data())[stage.name]

    @staticmethod
    async def get_kb_builder(
        stage: Type[BaseStage],
        state: FSMContext,
    ) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()
        checked_interests = await BaseStage.get_interests(stage, state)
        interest_page_i: int = await BaseStage.get_page_i(state)

        for interest in INTEREST_PAGES[interest_page_i]:
            prefix = (CHECK_MARK_EMOJI if interest in checked_interests
                      else "")

            builder.button(
                    text=prefix + interest,
                    callback_data=f"interest_{interest}",
                    )

        builder.adjust(2)

        # if interest_page_i == 0:
        #     left_arrow_button = InlineKeyboardButton(
        #         text="✖️",
        #         callback_data=DummyCallbackFactory(),
        #     )
        # else:
        #     left_arrow_button = InlineKeyboardButton(
        #         text="⬅️",
        #         callback_data=f"gopage_{interest_page_i - 1}",
        #     )

        # page_index_button = InlineKeyboardButton(
        #     text=f"{interest_page_i + 1}/{NO_INTEREST_PAGES}",
        #     callback_data=DummyCallbackFactory(),
        # )

        # if interest_page_i + 1 == NO_INTEREST_PAGES:
        #     right_arrow_button = InlineKeyboardButton(
        #         text="✖️",
        #         callback_data="pass",
        #     )
        # else:
        #     right_arrow_button = InlineKeyboardButton(
        #         text="➡",
        #         callback_data=f"gopage_{interest_page_i + 1}",
        #     )

        # builder.row(
        #     left_arrow_button,
        #     page_index_button,
        #     right_arrow_button,
        # )

        # "submit" button
        builder.row(
                InlineKeyboardButton(
                    text="📍подтвердить📍",
                    callback_data="submit_interests",
                )
            )

        return builder

    @staticmethod
    async def get_kb(
        stage: Type[BaseStage], state: FSMContext) -> InlineKeyboardMarkup:
        return (await stage.get_kb_builder(stage, state)).as_markup()

    @staticmethod
    async def get_submit_kb(
        stage: Type[BaseStage],
        interests: Iterable[str],
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for interest in interests:
            builder.button(
                text=CHECK_MARK_EMOJI + interest,
                # TODO:
                # no callback
                callback_data=DummyCallbackFactory()
            )

        builder.adjust(1)
        return builder.as_markup()


    @staticmethod
    async def get_question_args(
        stage: Type[BaseStage],
        state: FSMContext,
    ) -> Dict:
        return {
            "text": stage.question_text,
            "reply_markup": await BaseStage.get_kb(stage, state),
        }

    @staticmethod
    async def prepare_base(
        stage: StageType,
        state: FSMContext,
    ) -> None:
        await state.update_data(**{stage.name: list()})
        await BaseStage.set_page_i(state, 0)
        await Stage.bot.send_message(
            await get_id(state),
            **(await BaseStage.get_question_args(stage, state)),
        )

    @staticmethod
    async def process_callback_check_interest(
        stage: Type[BaseStage],
        callback: types.CallbackQuery,
        state: FSMContext,
    ) -> None:
        interests = await BaseStage.get_interests(stage, state)
        target_interest = callback.data.split('_', maxsplit=1)[1]

        if target_interest in interests:
            interests.remove(target_interest)
        else:
            if len(interests) == NO_INTERESTS:
                # Too much interests

                await callback.answer(
                    text="Превышено допустимое количество интересов")
                return

            interests.append(target_interest)

        # TODO: ???
        await state.update_data(**{stage.name: interests})

        await callback.message.edit_text(
            **(await BaseStage.get_question_args(stage, state)))
        await callback.answer()

    @staticmethod
    async def process_callback_go_page(
        stage: Type[BaseStage],
        callback: types.CallbackQuery,
        state: FSMContext,
    ) -> None:
        await BaseStage.set_page_i(
            state,
            int(callback.data.split('_', maxsplit=1)[1])
        )

        await callback.message.edit_text(
            **(await BaseStage.get_question_args(stage, state)))
        await callback.answer()

    @staticmethod
    async def process_callback_submit(
        stage: Type[BaseStage],
        callback: types.CallbackQuery,
        state: FSMContext,
    ):
        interests = await BaseStage.get_interests(stage, state)

        if len(interests) < NO_INTERESTS:
            await callback.answer(
                    text=f"Недостаточно интересов (должно быть {NO_INTERESTS})")
            return

        await next_stage(
            stage,
            state,
        )

        await callback.answer()

        await callback.message.edit_text(
            text=stage.submit_text,
            reply_markup=await BaseStage.get_submit_kb(stage, interests),
        )



    @staticmethod
    def register_base(
        stage: Type[BaseStage],
        router: Router,
    ) -> None:
        router.callback_query.register(
            stage.process_callback_check_interest,
            F.data.startswith("interest_"),
            stage.state,
        )

        router.callback_query.register(
            stage.process_callback_go_page,
            F.data.startswith("gopage_"),
            stage.state,
        )

        router.callback_query.register(
            stage.process_callback_submit,
            F.data=="submit_interests",
            stage.state,
        )
