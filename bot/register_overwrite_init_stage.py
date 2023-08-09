from stage import Stage
from get_id import get_id
from stage_order import prepare_stage_and_state
from overwrite.start import OverwriteStartStage

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from db.match import get_user_by_telegram_id_2
from db.user import User
from profile import Profile


OVERWRITE_PROFILE_TEXT = "Редактировать свою анкету"
GET_PROFILE_TEXT = "Моя анкета"

OVERWRITE_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=OVERWRITE_PROFILE_TEXT)],
        [KeyboardButton(text=GET_PROFILE_TEXT)],
    ],
    resize_keyboard=True,
)


class RegisterOverwriteInitSubstage(Stage):
    @staticmethod
    async def prepare(state: FSMContext) -> None:
        await Stage.bot.send_message(
            await get_id(state),
            "Ты успешно зарегистрирован! Теперь тебе доступно редактирование анкеты",
            reply_markup=OVERWRITE_KB,
        )

    @staticmethod
    async def process_overwrite(
        _: Message,
        state: FSMContext,
    ) -> None:
        await prepare_stage_and_state(OverwriteStartStage, state)

    @staticmethod
    async def process_get_my_profile(
        message: Message,
        state: FSMContext,
    ) -> None:
        user: User = await get_user_by_telegram_id_2(
            message.from_user.id, Stage.async_session)

        await Profile.send_to_yourself(user)

    @staticmethod
    async def process_delete_my_profile(
        message: Message,
        state: FSMContext,
    ) -> None:
        # user: User = await get_user_by_telegram_id_2( #     message.from_user.id, Stage.async_session)

        # async with Stage.async_session() as session:
        #     async with session.begin():
        #         await session.delete(user)

        await state.clear()

    @staticmethod
    def register(router: Router) -> None:
        router.message.register(
            RegisterOverwriteInitSubstage.process_overwrite,
            F.text==OVERWRITE_PROFILE_TEXT,
        )

        router.message.register(
            RegisterOverwriteInitSubstage.process_get_my_profile,
            F.text==GET_PROFILE_TEXT,
        )

        router.message.register(
            RegisterOverwriteInitSubstage.process_delete_my_profile,
            F.text=="delete_my_profile_secret_text_83458938459",
        )
