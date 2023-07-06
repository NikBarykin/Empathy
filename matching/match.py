from user_state import UserState
from matching.keyboards import (
        get_reply_kb,
        get_inline_kb,
        )

from engine import find_match

from aiogram import types
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import (
        async_sessionmaker,
        AsyncSession,
        )


async def process_match(
        message: types.Message,
        state: FSMContext,
        async_session: async_sessionmaker[AsyncSession],
    ):
    telegram_id = message.from_user.id
    partner = await find_match(telegram_id, async_session)

    if partner is None:
        await message.reply(
                text="На данный момент подходящих партнеров не найдено.",
                reply_markup=get_reply_kb())
        return

    text = (f"{partner.name}, {partner.age}\n"
            f"{partner.self_description}")

    await message.answer_photo(
        partner.photo,
        caption=text,
        reply_markup=get_inline_kb(telegram_id, partner.telegram_id))

    await state.set_state(UserState.rates)


async def process_anticipate_match(message: types.Message):
    await message.reply("Сначала поставьте оценку предыдущему кандидату")
