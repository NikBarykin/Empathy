from typing import Type
import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message, UserProfilePhotos, FSInputFile)
from aiogram.methods import GetUserProfilePhotos, SendPhoto

from stage import Stage

from engine.user import update_field

from utils.message_value_getters.photo import first_photo_getter
from utils.execute_method import execute_method

from user_stages.field_stages.produce import produce_field_stage

from .keyboard import get_kb
from .filter import PHOTO_FILTER
from .constants import (
    ADD_PROFILE_PHOTO_TEXT, PREPARE_TEXT,
    get_profile_photo_path, PROFILE_PHOTO_DIR,
)


def make_photo_stage(stage_name_arg: str) -> Type[Stage]:
    """Create and return photo-stage"""
    Base = produce_field_stage(
        stage_name_arg=stage_name_arg,
        field_name_arg="photo",
        prepare_text_arg=PREPARE_TEXT,
        value_getter_arg=first_photo_getter,
        inline_kb_getter_arg=None,
        reply_kb_getter_arg=get_kb,
        invalid_value_text_arg="Ошибка",
        message_filter_arg=PHOTO_FILTER,
    )

    async def process_profile_photo(
        message: Message,
        state: FSMContext,
    ) -> Message:
        """
            Use photo from user's telegram-account.
            Return next-stage prepare-result.
        """
        actor_id = message.from_user.id

        profile_photos: UserProfilePhotos | None = await execute_method(
            GetUserProfilePhotos(
                user_id=actor_id,
                offset=0,
                limit=1,
            ),
            logger=Base._logger,
        )

        if profile_photos is None:
            # some error happened
            return await Base._process_invalid_value(message, state)

        photo_id = profile_photos.photos[0][-1].file_id

        # Download user's profile photo in case it gets deleted from user's telegram account
        saved_photo_path: str = get_profile_photo_path(f"{photo_id}.jpg")

        await Stage.bot.download(photo_id, saved_photo_path)

        photo = FSInputFile(saved_photo_path)

        photo_message: Message | None = await execute_method(
            SendPhoto(
                chat_id=actor_id,
                photo=photo,
            ),
            logger=Base._logger,
        )

        if photo_message is None:
            # some error happened
            return await Base._process_invalid_value(message, state)

        photo_id = photo_message.photo[0].file_id

        await update_field(
            id=actor_id,
            field_name="photo",
            value=photo_id,
        )

        Base._logger.debug(
            "%s added photo from telegram profile", actor_id)

        return await Base.next_stage.prepare(state)

    base_register_method = Base.register

    def advanced_register(router: Router) -> None:
        # create directory for saving profile photos
        if not os.path.exists(PROFILE_PHOTO_DIR):
            os.makedirs(PROFILE_PHOTO_DIR)

        # order matters
        router.message.register(
            process_profile_photo,
            F.text==ADD_PROFILE_PHOTO_TEXT,
            Base._main_state,
        )

        base_register_method(router)

    # Replace 'register'-method.
    # We can't use inheritance, because
    # in this case 'next_stage' and 'prev-stage'
    # attributes of Derived-stage are needed to be passed to Base-class
    Base.register = advanced_register

    return Base
