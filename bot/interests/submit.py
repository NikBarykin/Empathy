from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from constants import CHECK_MARK_EMOJI, INTERESTS, NO_INTERESTS
from personal import photo
from registration_end import process_end
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from user_state import UserState

from .prepare import get_interests, partner_interests


async def get_inline_kb(
        state: FSMContext,
        ) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for interest in await get_interests(state):
        builder.button(
                text=interest + CHECK_MARK_EMOJI,
                # no callback
                callback_data="pass",
                )

    builder.adjust(1)
    return builder.as_markup()


async def process_submit(
    message: Message,
    state: FSMContext,
) -> None:
    text: str = ("Твои интересы:" if not await partner_interests(state)
                 else "Ожидаемые интересы")
    await message.edit_text(
            text=text,
            reply_markup=await get_inline_kb(state),
            )


async def prepare_further(
    message: Message,
    bot: Bot,
    state: FSMContext,
    async_session: async_sessionmaker[AsyncSession],
) -> None:
    if await partner_interests(state):
        await process_end(
            bot,
            (await state.get_data())['telegram_id'],
            state,
            async_session,
        )
    else:
        await photo.prepare(
            message,
            state,
        )


async def process_callback_submit_same(
    callback: types.CallbackQuery,
    bot: Bot,
    state: FSMContext,
    async_session: async_sessionmaker[AsyncSession],
):
    await state.update_data(
        preferred_partner_interests=(await state.get_data())['interests'])
    await process_callback_submit(callback, bot, state, async_session)


async def process_callback_submit(
    callback: types.CallbackQuery,
    bot: Bot,
    state: FSMContext,
    async_session: async_sessionmaker[AsyncSession],
):
    interests = await get_interests(state)

    if len(interests) < NO_INTERESTS:
        await callback.answer(
                text=f"Недостаточно интересов (должно быть {NO_INTERESTS})")
        return

    await process_submit(
            callback.message,
            state,
            )

    await callback.answer()

    await prepare_further(callback.message, bot, state, async_session)
