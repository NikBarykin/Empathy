"""Managing keyboards"""
from stages.stage import Stage

from aiogram.types import ReplyKeyboardMarkup


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
    # await Stage.bot.delete_message(chat_id=chat_id, message_id=message.message_id)
