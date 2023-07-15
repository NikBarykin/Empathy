from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from db.match import find_match, get_user_by_telegram_id
from db.user import User
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from user_state import UserState

from matching.keyboards import get_inline_kb


async def process_no_partner_yet(
    bot: Bot,
    user_telegram_id: int,
    async_session: async_sessionmaker[AsyncSession],
) -> None:
    await User.put_in_waiting_pool(
        telegram_id=user_telegram_id, async_session=async_session)

    await bot.send_message(
            user_telegram_id,
            text=("На данный момент подходящих партнеров не найдено. "
                  "Когда появятся подходящие варианты, мы обязательно тебе напишем!😉"),
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
        await process_no_partner_yet(bot, user_telegram_id, async_session)
    else:
        await process_found_partner(bot, user_telegram_id, partner)
