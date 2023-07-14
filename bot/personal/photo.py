from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup
from user_state import UserState

from personal import self_description

ADD_PROFILE_PHOTO_TEXT = "Добавить фотографию из профиля"


def get_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
            keyboard= [[types.KeyboardButton(text=ADD_PROFILE_PHOTO_TEXT)]],
            resize_keyboard=True,
            one_time_keyboard=True,
            )


async def prepare(
        message: Message,
        state: FSMContext,
        ) -> None:
    await message.answer(
            "Добавь фотографию",
            reply_markup=get_kb())
    await state.set_state(UserState.photo)


async def process_photo(
        message: Message,
        state: FSMContext,
        photo_id: int,
        ):
    await state.update_data(photo=photo_id)
    await message.answer_photo(
            photo=photo_id,
            )
    await message.answer("Отлично выглядишь!")

    await self_description.prepare(message, state)


async def process_explicitly_choosen_photo(
        message: Message,
        state: FSMContext,
        ) -> None:
    await process_photo(
            message,
            state,
            message.photo[0].file_id,
            )


async def process_profile_photo(
        message: Message,
        state: FSMContext,
        ):
    profile_photos = (
            await message.from_user.get_profile_photos(
                offset=0,
                limit=1,
                )
            ).photos

    photo_id = profile_photos[0][0].file_id

    await process_photo(
            message,
            state,
            photo_id,
            )
