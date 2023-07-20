from simple_get_stage import produce_simple_get_stage
from empty_reply_markup_getter import get_empty_reply_markup
from one_alternative_from_filter import OneAlternativeFromFilter

from stage import Stage
from user_state import UserState

from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from stage_order import next_stage
from constants import CITIES


CityStage = produce_simple_get_stage(
    stage_name="город",
    question_text="Твой город?",
    question_reply_markup_getter=get_empty_reply_markup,
    invalid_value_text="Я не знаю такого города",
    data_update_value_getter=lambda message: message.text.lower(),
    message_filter=OneAlternativeFromFilter(CITIES),
)




# class CityStage(Stage):
#     state = State()
#     name: str = "город"

#     @staticmethod
#     async def prepare(user_id: int, state: FSMContext) -> None:
#         await Stage.bot.send_message(user_id, "Твой город?")

#     @staticmethod
#     def register(router: Router) -> None:
#         router.message.register(
#             CityStage.process,
#             F.text.lower().in_(CITIES),
#             CityStage.state,
#         )

#         router.message.register(
#             CityStage.process_invalid_value,
#             CityStage.state,
#         )

#     @staticmethod
#     async def process(
#         message: Message,
#         state: FSMContext,
#     ) -> None:
#         await state.update_data(**{CityStage.name: message.text})
#         await next_stage(CityStage, message.from_user.id, state)

#     @staticmethod
#     async def process_invalid_value(message: types.Message):
#         await message.reply("Я не знаю такого города")


from personal.relationship_goal import get_kb
from user_state import UserState

from aiogram.types import Message
from aiogram.fsm.context import FSMContext


async def prepare(message: Message, state: FSMContext):
    await message.answer("Твой город")
    await state.set_state(UserState.city)


# TODO: allow mistakes and add more cities
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text.lower())

    await message.answer(
            "Твоя цель",
            reply_markup=get_kb()
            )
    await state.set_state(UserState.relationship_goal)


async def process_invalid_city(message: Message):
    await message.reply("Я не знаю такого города")
