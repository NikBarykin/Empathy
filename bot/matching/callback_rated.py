from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from constants import DISLIKE_EMOJI, LIKE_EMOJI
from db.match import check_liked, get_user_by_telegram_id
from db.rating import Rating
from db.user import User
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from user_state import UserState

from matching.match import get_next_match
from matching.rating_callback_factory import RatingCallbackFactory


def get_already_rated_kb(
        liked: bool
        ) -> types.InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
            text=(LIKE_EMOJI if liked else DISLIKE_EMOJI),
            callback_data=f"already_rated",
            )
    return keyboard.as_markup()


async def insert_rating(
        liked: bool,
        subj: User,
        obj: User,
        session: AsyncSession,
        ) -> None:
    async with session.begin():
        session.add(
                Rating(
                    liked,
                    subj,
                    obj,
                    )
                )


async def process_callback_rated(
        callback: types.CallbackQuery,
        callback_data: RatingCallbackFactory,
        bot: Bot,
        async_session: async_sessionmaker[AsyncSession],
        ):

    async with async_session() as session:
        subj = await get_user_by_telegram_id(
                callback_data.subj_telegram_id,
                session)

        obj = await get_user_by_telegram_id(
                callback_data.obj_telegram_id,
                session)

        liked: bool = callback_data.liked

        await insert_rating(
                liked,
                subj,
                obj,
                session,
                )

        await callback.message.edit_reply_markup(
                reply_markup=get_already_rated_kb(liked),
                )

        # check for mutual sympathy
        liked_back: bool = await check_liked(obj, subj, session)
        if liked and liked_back:

            reply_text = "🔥У вас взаимная симпатия с @{}🔥"

            await bot.send_message(
                    obj.id,
                    text=reply_text.format(subj.telegram_handle),
                    )

            await bot.send_message(
                    subj.id,
                    text=reply_text.format(obj.telegram_handle),
                    )

    await callback.answer()

    await get_next_match(
            bot=bot,
            user_telegram_id=callback_data.subj_telegram_id,
            async_session=async_session,
            )


async def process_callback_already_rated(
        callback: types.CallbackQuery,
        ):
    await callback.answer(text="Вы уже оценили этого человека")
