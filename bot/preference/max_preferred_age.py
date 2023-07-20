from simple_get_stage import produce_simple_get_stage
from age_filter import AgeFilter


MaxPreferredAgeStage = produce_simple_get_stage(
    stage_name="Максимальный возраст партнера",
    question_text="Укажи максимальный возраст для твоего партнера",
    invalid_value_text="Некорректное значение возраста",
    data_update_value_getter=lambda message: int(message.text),
    message_filter=AgeFilter(),
)

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
