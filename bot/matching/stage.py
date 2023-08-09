from stage import Stage
from stage_order import next_stage
from get_id import get_id
import logging

from db.rating import Rating
from db.user import User
from db.match import check_liked, find_match, get_user_by_telegram_id, get_user_by_telegram_id_2

from profile import Profile

from matching.keyboards import get_inline_kb
from matching.rating_callback_factory import RatingCallbackFactory

from aiogram import Router, types, F
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from constants import LIKE_EMOJI, DISLIKE_EMOJI

from sqlalchemy.ext.asyncio import AsyncSession

from get_last_profile_id import set_last_profile_id
from contextlib import suppress
from sqlalchemy.exc import IntegrityError
from aiogram.exceptions import TelegramBadRequest


def get_already_rated_kb(
        liked: bool
        ) -> types.InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
            text=(LIKE_EMOJI if liked else DISLIKE_EMOJI),
            callback_data="already_rated",
            )
    return keyboard.as_markup()


async def insert_rating(
        liked: bool,
        subj: User,
        obj: User,
        async_session,
        ) -> None:
        with suppress(IntegrityError):
            async with async_session() as session:
                async with session.begin():
                    await session.merge(
                            Rating(
                                liked,
                                subj,
                                obj,
                                )
                            )


class MatchStage(Stage):
    state = State()
    name: str = "match"

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        await MatchStage.get_next_match(state, await get_id(state))

    @staticmethod
    async def process_no_partner_yet(
        user_telegram_id: int,
    ) -> None:
        await Stage.bot.send_message(user_telegram_id, text=(
            "На данный момент партнеров не найдено. "
            "Когда появятся подходящие варианты, мы обязательно тебе напишем!😉"))

    @staticmethod
    async def process_found_partner(
        state: FSMContext,
        user_telegram_id: int,
        partner: User,
    ) -> None:
        user: User = await get_user_by_telegram_id_2(
            user_telegram_id, Stage.async_session)

        await User.remove_from_waiting_pool(
                telegram_id=user_telegram_id, async_session=Stage.async_session)

        profile = Profile(partner)

        logging.debug(f"Found a partner {partner} for {user_telegram_id}, sending its profile")

        try:
            message: Message = await profile.send_to(
                user_telegram_id,
                reply_markup=get_inline_kb(
                    user_telegram_id, partner.id),
            )

            await set_last_profile_id(state, message.message_id)
        except TelegramBadRequest:
            subj = None
            async with Stage.async_session() as session:
                subj = await get_user_by_telegram_id(
                        user_telegram_id,
                        session)

            obj = None
            async with Stage.async_session() as session:
                obj = await get_user_by_telegram_id(
                        partner.id,
                        session)

            await insert_rating(
                    False,
                    subj,
                    obj,
                    Stage.async_session,
                    )
            await MatchStage.prepare(state)

    @staticmethod
    async def get_next_match(
        state: FSMContext,
        user_telegram_id: int,
        do_nothing_on_not_found: bool = False,
    ):
        partner = await find_match(user_telegram_id, Stage.async_session)

        if partner is None:
            await User.put_in_waiting_pool(
                telegram_id=user_telegram_id, async_session=Stage.async_session)

            if not do_nothing_on_not_found:
                await MatchStage.process_no_partner_yet(user_telegram_id)
        else:
            await MatchStage.process_found_partner(state, user_telegram_id, partner)

    @staticmethod
    async def process_callback_rated(
        callback: types.CallbackQuery,
        callback_data: RatingCallbackFactory,
        state: FSMContext,
    ) -> None:
        subj = None
        async with Stage.async_session() as session:
            subj = await get_user_by_telegram_id(
                    callback_data.subj_telegram_id,
                    session)

        obj = None
        async with Stage.async_session() as session:
            obj = await get_user_by_telegram_id(
                    callback_data.obj_telegram_id,
                    session)

        liked: bool = callback_data.liked

        await insert_rating(
                liked,
                subj,
                obj,
                Stage.async_session,
                )

        await callback.message.edit_reply_markup(
                reply_markup=get_already_rated_kb(liked),
                )

        # check for mutual sympathy

        async with Stage.async_session() as session:
            liked_back: bool = await check_liked(obj, subj, session)

        if liked and liked_back:

            reply_text = "🔥У вас взаимная симпатия с @{}🔥"

            await Stage.bot.send_photo(
                obj.id,
                photo=subj.photo,
                caption=reply_text.format(subj.telegram_handle),
            )

            await Stage.bot.send_photo(
                subj.id,
                photo=obj.photo,
                caption=reply_text.format(obj.telegram_handle),
            )

        await callback.answer()
        await MatchStage.prepare(state)

    @staticmethod
    async def process_callback_already_rated(
            callback: types.CallbackQuery,
            ):
        await callback.answer(text="Вы уже оценили этого человека")

    @staticmethod
    def register(router: Router) -> None:
        router.callback_query.register(
            MatchStage.process_callback_rated,
            RatingCallbackFactory.filter(),
            MatchStage.state,
        )

        router.callback_query.register(
            MatchStage.process_callback_already_rated,
            F.data=="already_rated",
            MatchStage.state,
        )
