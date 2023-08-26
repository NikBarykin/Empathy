"""Get text-field from aiogram.types.Message instance"""
from aiogram.types import Message


async def raw_getter(message: Message):
    """Get message's text without any modification"""
    return message.text


async def lower_getter(message: Message):
    """Get message's text and lower it"""
    return message.text.lower()


async def int_getter(message: Message):
    """Get message's text and convert it to int"""
    return int(message.text)
