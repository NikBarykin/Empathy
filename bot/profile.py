from dummy_callback_factory import DummyCallbackFactory

from db.user import User
from stage import Stage
from dataclasses import dataclass

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Твоя анкета",
        callback_data=DummyCallbackFactory(),
    )
    return builder.as_markup()


class Profile:
    photo_id: str
    text: str

    def __init__(self, user: User):
        self.photo_id = user.photo
        self.text = (f"{user.name}, {user.age}\n"
                     f"{user.self_description}")

    async def send_to(self, user_id: int, reply_markup=None) -> Message:
        return await Stage.bot.send_photo(
            user_id,
            photo=self.photo_id,
            caption=self.text,
            reply_markup=reply_markup,
        )

    @staticmethod
    async def send_to_yourself(user: User) -> Message:
        return await Profile(user).send_to(
            user.id,
            reply_markup=get_kb(),
        )
