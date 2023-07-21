from stage import Stage
from command_start import get_id
from stage_order import prepare_stage_and_state
from overwrite.start import OverwriteStartStage

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext


OVERWRITE_PROFILE_TEXT = "Редактировать свою анкету"

OVERWRITE_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=OVERWRITE_PROFILE_TEXT)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


class RegisterOverwriteInitSubstage(Stage):
    @staticmethod
    async def prepare(state: FSMContext) -> None:
        await Stage.bot.send_message(
            await get_id(state),
            "Ты успешно зарегистрирован! Теперь тебе доступно редактирование профиля",
            reply_markup=OVERWRITE_KB,
        )

    @staticmethod
    async def process(
        _: Message,
        state: FSMContext,
    ) -> None:
        await prepare_stage_and_state(OverwriteStartStage, state)

    @staticmethod
    def register(router: Router) -> None:
        router.message.register(
            RegisterOverwriteInitSubstage.process,
            F.text == OVERWRITE_PROFILE_TEXT,
        )
