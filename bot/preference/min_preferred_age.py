from simple_get_stage import produce_simple_get_stage
from age_filter import AgeFilter


MinPreferredAgeStage = produce_simple_get_stage(
    stage_name="минимальный возраст партнера",
    question_text="Укажи минимальный возраст для твоего партнера",
    invalid_value_text="Некорректное значение возраста",
    data_update_value_getter=lambda message: int(message.text),
    message_filter=AgeFilter(),
)

from stage import Stage
from user_state import UserState

from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from stage_order import next_stage


# class MinAgeStage(Stage):
#     state = State()
#     name: str = "минимальный возраст партнера"

#     @staticmethod
#     async def prepare(user_id: int, state: FSMContext) -> None:
#         await Stage.bot.send_message(user_id, "Минимальный возраст партнера")

#     @staticmethod
#     def register(router: Router) -> None:
#         router.message.register(
#             MinAgeStage.process,
#             F.text.isnumeric(),
#             lambda message: 18 <= int(message.text) <= 99,
#             MinAgeStage.state,
#         )

#         router.message.register(
#             MinAgeStage.process_invalid_value,
#             MinAgeStage.state,
#         )

#     @staticmethod
#     async def process(
#         message: Message,
#         state: FSMContext,
#     ) -> None:
#         await state.update_data(**{MinAgeStage.name: message.text})
#         await next_stage(MinAgeStage, message.from_user.id, state)

#     @staticmethod
#     async def process_invalid_value(message: types.Message):
#         await message.reply("Некорректное значение возраста")


# TODO: invalid value
async def process_min_preferred_age(
        message: Message,
        state: FSMContext,
        ):
    await state.update_data(min_preferred_age=int(message.text))

    # max-preferred-age
    await message.answer("Укажи максимальный возраст партнера")
    await state.set_state(UserState.max_preferred_age)
