"""Managing keyboards"""
from typing import Iterable

from stage import Stage

from aiogram.types import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton)


class RowKeyboard(ReplyKeyboardMarkup):
    """Reply-keyboard with one row containing buttons with given texts"""
    def __init__(
        self,
        *button_texts: str,
        one_time_keyboard: bool=True,
        resize_keyboard: bool=True,
    ):
        super().__init__(
            keyboard=[[
                KeyboardButton(text=button_text)
                for button_text in button_texts
            ]],
            one_time_keyboard=one_time_keyboard,
            resize_keyboard=resize_keyboard,
        )


def concat_reply_keyboards(
    kb1: ReplyKeyboardMarkup,
    kb2: ReplyKeyboardMarkup,
) -> ReplyKeyboardMarkup:
    if kb1 is None:
        return kb2
    if kb2 is None:
        return kb1
    return ReplyKeyboardMarkup(
        keyboard=kb1.keyboard + kb2.keyboard,
        one_time_keyboard=kb1.one_time_keyboard,
        resize_keyboard=kb1.resize_keyboard,
    )


async def send_reply_kb(chat_id: int, kb: ReplyKeyboardMarkup):
    message = await Stage.bot.send_message(
        chat_id=chat_id, text="⚡️", reply_markup=kb)
    return message


async def remove_reply_keyboard(chat_id: int):
    message = await Stage.bot.send_message(
        chat_id=chat_id, text=".", reply_markup=ReplyKeyboardRemove())
    await Stage.bot.delete_message(
        chat_id=chat_id, message_id=message.message_id)
