from stage import Stage
from simple_get_stage import produce_simple_get_stage
from .min_preferred_age import MinPreferredAgeStage


from age_filter import AgeFilter

from aiogram.types import Message
from aiogram.fsm.context import FSMContext


# TODO: process max age less than min age
MaxPreferredAgeStage = produce_simple_get_stage(
    stage_name="максимальный возраст партнера",
    question_text="Укажи максимальный возраст для твоего партнера",
    invalid_value_text="Некорректное значение возраста",
    data_update_value_getter=lambda message: int(message.text),
    message_filter=AgeFilter(),
)


# class MaxPreferredAgeStage(MaxPreferredAgeStageBase):
#     @staticmethod
#     async def check_if_min_age_greater_than_max_age(message: Message, state: FSMContext) -> bool:
#         max_preferred_age: int = int(message.text)
#         min_preferred_age: int = (await state.get_data())[MinPreferredAgeStage.name]
#         return min_preferred_age > max_preferred_age

#     @staticmethod
#     async def process(message: Message, state: FSMContext) -> None:
#         if MaxPreferredAgeStage.check_if_min_age_greater_than_max_age(message, state):
#             message.reply("Минимальный возраст больше максимального")
#         min_preferred_age: int = (await state.get_data())[MinPreferredAgeStage.name]
#         if int(message.text) < min


# import registration_end
# from aiogram import Bot, types
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message
# from db.user import User
# from interests.prepare import prepare_preferred_partner_interests
# from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
# from user_state import UserState


# async def process_max_preferred_age(
#         message: types.Message,
#         bot: Bot,
#         state: FSMContext,
#         async_session: async_sessionmaker[AsyncSession],
#         ):
#     await state.update_data(max_preferred_age=int(message.text))
#     await prepare_preferred_partner_interests(
#         message,
#         state,
#     )
