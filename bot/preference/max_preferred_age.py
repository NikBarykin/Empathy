import registration_end
from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from db.user import User
from interests.prepare import prepare_preferred_partner_interests
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from user_state import UserState


async def process_max_preferred_age(
        message: types.Message,
        bot: Bot,
        state: FSMContext,
        async_session: async_sessionmaker[AsyncSession],
        ):
    await state.update_data(max_preferred_age=int(message.text))
    await prepare_preferred_partner_interests(
        message,
        state,
    )
