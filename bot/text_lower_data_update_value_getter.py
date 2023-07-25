from aiogram.types import Message


def text_lower_data_update_value_getter(message: Message) -> str:
    return message.text.lower()
