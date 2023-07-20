from simple_get_stage import produce_simple_get_stage
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message
from constants import SEXES
from stage_order import next_stage
from stage import Stage
from one_alternative_from_filter import OneAlternativeFromFilter


async def get_kb(_: FSMContext) -> types.ReplyKeyboardMarkup:
    kb = [
            [types.KeyboardButton(text=sex) for sex in SEXES]
    ]
    return types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True,
            )

SexStage = produce_simple_get_stage(
    stage_name="пол",
    question_text="Твой пол?",
    question_reply_markup_getter=get_kb,
    invalid_value_text=f"Принимаются только значения {SEXES}",
    data_update_value_getter=lambda message: message.text,
    message_filter=OneAlternativeFromFilter(SEXES),
)



# class SexStage(Stage):
#     state = State()
#     name: str = "пол"

#     @staticmethod
#     async def prepare(user_id: int, state: FSMContext) -> None:
#         await Stage.bot.send_message(user_id, "Твой пол?", reply_markup=get_kb())

#     @staticmethod
#     def register(router: Router) -> None:
#         router.message.register(
#             SexStage.process,
#             F.text.lower().in_(SEXES),
#             SexStage.state,
#         )

#         router.message.register(
#             SexStage.process_invalid_value,
#             SexStage.state,
#         )

#     @staticmethod
#     async def process(
#         message: Message,
#         state: FSMContext,
#     ) -> None:
#         # TODO: enum
#         await state.update_data(**{SexStage.name: message.text.lower()})
#         await next_stage(SexStage, message.from_user.id, state)

#     @staticmethod
#     async def process_invalid_value(message: types.Message):
#         await message.reply("Некорректное значение")


async def process_sex(
        message: types.Message,
        state: FSMContext
        ):
    await state.update_data(sex=message.text.lower())
    await city.prepare(message, state)


async def process_invalid_sex(message: types.Message):
    await message.reply("Некорректное значение")
