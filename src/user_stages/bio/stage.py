from typing import Type

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from stage import Stage, go_next_stage

from utils.field_base import produce_field_stage
from utils.message_value_getters.text import raw_getter

from engine.user import update_field

from .keyboard import get_kb
from .filter import BIO_FILTER
from .logic import get_bio_from_telegram
from .constants import USE_BIO_FROM_TELEGRAM_TEXT, TARGET_FIELD_NAME


def make_bio_stage(stage_name_arg: str, skip_if_field_presented: bool) -> Type[Stage]:
    Base = produce_field_stage(
        stage_name_arg=stage_name_arg,
        field_name_arg=TARGET_FIELD_NAME,
        prepare_text_arg="Напиши немного о себе",
        value_getter_arg=raw_getter,
        inline_kb_getter_arg=None,
        reply_kb_getter_arg=get_kb,
        invalid_value_text_arg="Ошибка",
        filter_arg=BIO_FILTER,
        skip_if_field_presented_arg=skip_if_field_presented,
    )

    class BioStage(Base):
        @staticmethod
        async def process_profile_bio(
            message: Message,
            state: FSMContext,
        ) -> None:
            actor_id = message.from_user.id
            bio = await get_bio_from_telegram(user_id=actor_id)
            await update_field(
                id=actor_id,
                field_name=TARGET_FIELD_NAME,
                value=bio,
            )
            Base._logger("Updated bio from telegram-profile for %s", actor_id)
            return await go_next_stage(departure=BioStage, state=state)

        @staticmethod
        def register(router: Router) -> None:
            # order matters
            router.message.register(
                BioStage.process_profile_bio,
                F.text==USE_BIO_FROM_TELEGRAM_TEXT,
                BioStage._main_state,
            )
            # Crutch: it is important to pass next_stage value to the Base
            Base.next_stage = BioStage.next_stage
            Base.register(router)

    return BioStage
