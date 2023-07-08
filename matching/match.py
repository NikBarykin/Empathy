from user import User
from user_state import UserState
from matching.keyboards import (
        get_inline_kb,
        )

from engine import find_match

from aiogram import (
        types,
        Bot,
        )
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import (
        async_sessionmaker,
        AsyncSession,
        )


async def process_no_partner_yet(
        # TODO: chat_id instead of message
        bot: Bot,
        user_telegram_id: int,
        ) -> None:
    # TODO: put user in a waiting pool
    await bot.send_message(
            user_telegram_id,
            text="На данный момент подходящих партнеров не найдено.",
            reply_markup=types.ReplyKeyboardRemove())


async def process_found_partner(
        bot: Bot,
        user_telegram_id: int,
        partner: User,
        ) -> None:

    text = (f"{partner.name}, {partner.age}\n"
            f"{partner.self_description}")

    await bot.send_photo(
            user_telegram_id,
            partner.photo,
            caption=text,
            reply_markup=get_inline_kb(user_telegram_id, partner.telegram_id),
            )


async def get_next_match(
        bot: Bot,
        user_telegram_id: int,
        async_session: async_sessionmaker[AsyncSession],
    ):
    partner = await find_match(user_telegram_id, async_session)

    if partner is None:
        await process_no_partner_yet(bot, user_telegram_id)
    else:
        await process_found_partner(bot, user_telegram_id, partner)
