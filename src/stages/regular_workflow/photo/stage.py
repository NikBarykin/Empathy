from typing import Type

from stages.stage import Stage, go_next_stage

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup

from message_value_getters.photo import first_photo_getter

from engine.user import update_field

from utils.id import get_id
from utils.field_base import produce_field_stage

from .keyboard import get_kb
from .filter import PHOTO_FILTER
from .constants import ADD_PROFILE_PHOTO_TEXT


def make_photo_stage(stage_name_arg: str) -> Type[Stage]:
    Base = produce_field_stage(
        stage_name_arg=stage_name_arg,
        field_name_arg="photo",
        prepare_text_arg="Добавь фотографию",
        value_getter_arg=first_photo_getter,
        inline_kb_getter_arg=None,
        reply_kb_getter_arg=get_kb,
        invalid_value_text_arg="Добавь фотографию (не файлом)",
        filter_arg=PHOTO_FILTER,
    )

    class PhotoStage(Base):
        @staticmethod
        async def process_profile_photo(
            message: Message,
            state: FSMContext,
        ) -> None:
            profile_photos = (
                    await message.from_user.get_profile_photos(
                        offset=0,
                        limit=1,
                        )
                    ).photos

            photo_id = profile_photos[0][0].file_id

            actor_id = await get_id(state)

            await update_field(
                id=actor_id,
                field_name="photo",
                value=photo_id,
            )

            PhotoStage._logger.debug(
                "%s added photo from telegram profile", actor_id)

            return await go_next_stage(departure=PhotoStage, state=state)

        @staticmethod
        def register(router: Router) -> None:
            # order matters
            router.message.register(
                PhotoStage.process_profile_photo,
                F.text==ADD_PROFILE_PHOTO_TEXT,
                PhotoStage._main_state,
            )
            Base.register(router)

    return PhotoStage
