from aiogram.types import Message


def parse_city_name(city_name: str) -> str:
    """Take raw city name, lower it and remove special characters"""
    return city_name.translate({ord(c): None for c in " -_"}).lower()


async def get_city_name(message: Message) -> str:
    """Take message-text and extract (if possible) city name from it"""
    return parse_city_name(message.text)
