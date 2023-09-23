"""Managing keyboards"""
from logging import Logger

from aiogram.types import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove,
    KeyboardButton, Message,
    InlineKeyboardMarkup, InlineKeyboardButton,
)

from aiogram.methods import SendMessage, DeleteMessage

from utils.execute_method import execute_method
from utils.dummy import DummyCallbackFactory


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


async def send_reply_kb(
    chat_id: int,
    kb: ReplyKeyboardMarkup,
    logger: Logger | None = None,
) -> Message:
    message = await execute_method(
        SendMessage(
            chat_id=chat_id, text="⚙️", reply_markup=kb),
        logger=logger,
    )
    return message


async def remove_reply_keyboard(
    chat_id: int,
    logger: Logger | None = None,
) -> Message:
    """
        Send fake message with 'ReplyKeyboardRemove' and instantly delete it.
        Return that fake message
    """
    message = await execute_method(
        SendMessage(
            chat_id=chat_id, text=".", reply_markup=ReplyKeyboardRemove()),
        logger=logger,
    )
    await execute_method(
        DeleteMessage(
            chat_id=chat_id, message_id=message.message_id),
        logger=logger,
    )
    return message


class DummyInlineKeyboard(InlineKeyboardMarkup):
    """
        Inline keyboard with one column
        (i.e. multiple rows each contains one button),
        containing buttons with given texts that ignore any clicks.
    """
    def __init__(self, *button_texts, **kwargs):
        super().__init__(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=button_text,
                        callback_data=DummyCallbackFactory().pack(),
                    )
                ]
                for button_text in button_texts
            ],
            **kwargs,
        )
