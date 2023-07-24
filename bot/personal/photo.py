from stage import Stage
from simple_get_stage import produce_simple_get_stage
from stage_order import next_stage
from get_id import get_id

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.filters import Text


ADD_PROFILE_PHOTO_TEXT = "Добавить фотографию из профиля"


async def has_profile_photo(state: FSMContext) -> bool:
    photos = (await Stage.bot.get_user_profile_photos(
        await get_id(state), offset=0, limit=1)).photos
    return len(photos) > 0


async def get_kb(state: FSMContext) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
            keyboard=([[types.KeyboardButton(text=ADD_PROFILE_PHOTO_TEXT)]]
                      if await has_profile_photo(state)
                      else []),
            resize_keyboard=True,
            one_time_keyboard=True,
            )


PhotoStageBase = produce_simple_get_stage(
    stage_name="фотография",
    question_text="Добавь фотографию",
    data_update_value_getter=lambda message: message.photo[0].file_id,
    message_filter=F.photo,
    invalid_value_text="Добавь фотографию (не файлом)",
    question_reply_markup_getter=get_kb,
)


class PhotoStage(PhotoStageBase):
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
        await state.update_data(**{PhotoStage.name: photo_id})
        await next_stage(PhotoStage, state)

    @staticmethod
    def register(router: Router) -> None:
        # order matters
        router.message.register(
            PhotoStage.process_profile_photo,
            Text(ADD_PROFILE_PHOTO_TEXT),
            PhotoStage.state,
        )
        PhotoStageBase.register(router)
