from simple_get_stage import produce_simple_get_stage
from age_filter import AgeFilter
from aiogram.fsm.context import FSMContext


AgeStage = produce_simple_get_stage(
    stage_name="возраст",
    question_text="Сколько тебе лет?",
    invalid_value_text="Некорректное значение возраста",
    data_update_value_getter=lambda message: int(message.text),
    message_filter=AgeFilter(),
)











from stage import Stage
from user_state import UserState
from personal.sex import get_kb

from stage_order import next_stage

from aiogram import types, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F


# class AgeStage(Stage):
#     state = State()
#     name: str = "age"

#     @staticmethod
#     async def prepare(user_id: int, state: FSMContext) -> None:
#         await Stage.bot.send_message(user_id, "Сколько тебе лет?")

#     @staticmethod
#     async def process(
#         message: Message,
#         state: FSMContext,
#     ) -> None:
#         await state.update_data(**{AgeStage.name: message.text})
#         await next_stage(AgeStage, message.from_user.id, state)

#     @staticmethod
#     async def process_invalid_age(message: Message):
#         # TODO: more clear comment
#         await message.reply("Возраст должен быть числом в промежутке от 18 до 99")

#     @staticmethod
#     def register(router: Router) -> None:
#         router.message.register(
#             AgeStage.process,
#                 # TODO: check
#             F.text.isnumeric(),
#             lambda message: 18 <= int(message.text) <= 99,
#             AgeStage.state,
#         )

#         router.message.register(
#             AgeStage.process_invalid_age,
#             AgeStage.state,
#         )


async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))

    await message.answer(
            "Твой пол?",
            reply_markup=get_kb())

    await state.set_state(UserState.sex)


async def process_invalid_age(message: Message):
    # TODO: more clear comment
    await message.reply("Некорректное значение")
