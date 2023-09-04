from aiogram.types import Message
from aiogram.filters import BaseFilter

from .constants import CITIES
from .message_value_getter import parse_city_name


class CityFilter(BaseFilter):
    """Does message contain valid city name in text field"""
    async def __call__(self, message: Message) -> bool:
        city_raw = message.text
        if city_raw is None:
            return None
        city_name = parse_city_name(city_raw)
        return city_name in CITIES
