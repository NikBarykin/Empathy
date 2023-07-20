from stage import Stage

from user_state import UserState
from stage_order import next_stage

from aiogram import Router, types
from aiogram.types import Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.state import State

from constants import RELATIONSHIP_GOALS


async def get_kb(state: FSMContext) -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for goal in RELATIONSHIP_GOALS:
        builder.button(text=goal)

    builder.adjust(2)

    return builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=True,
            )

from simple_get_stage import produce_simple_get_stage
from one_alternative_from_filter import OneAlternativeFromFilter


RelationshipGoalStage = produce_simple_get_stage(
    stage_name="цель отношений",
    question_text="Цель отношений?",
    question_reply_markup_getter=get_kb,
    invalid_value_text="Неизвестное значение",
    data_update_value_getter=lambda message: message.text,
    message_filter=OneAlternativeFromFilter(RELATIONSHIP_GOALS),
)


# class RelationshipGoalStage(Stage):
#     state = State()
#     name: str = "цель отношений"

#     @staticmethod
#     async def prepare(user_id: int, state: FSMContext) -> None:
#         await Stage.bot.send_message(
#             user_id,
#             "Цель отношений",
#             reply_markup = get_kb(),
#         )

#     @staticmethod
#     def register(router: Router) -> None:
#         router.message.register( RelationshipGoalStage.process,
#             F.text.in_(RELATIONSHIP_GOALS),
#             RelationshipGoalStage.state,
#         )

#         router.message.register(
#             RelationshipGoalStage.process_invalid_value,
#             RelationshipGoalStage.state,
#         )

#     @staticmethod
#     async def process(
#         message: Message,
#         state: FSMContext,
#     ) -> None:
#         await state.update_data(**{RelationshipGoalStage.name: message.text})
#         await next_stage(RelationshipGoalStage, message.from_user.id, state)

#     @staticmethod
#     async def process_invalid_value(message: Message):
#         await message.reply(
#             "Некорректное значение",
#             reply_markup=get_kb(),
#         )


async def process_relationship_goal(
        message: types.Message,
        state: FSMContext,
        ):
    await state.update_data(relationship_goal=message.text)

    await prepare_interests(message, state)


async def process_invalid_relationship_goal(
        message: types.Message,
        ):
    message.reply(
            "Некорректное значение",
            reply_markup=get_kb(),
            )
