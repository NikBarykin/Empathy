from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callback_factory import (
    CheckInterestCallbackFactory, SubmitCallbackFactory)


MIN_NO_INTERESTS: int = 3

QUESTION_TEXT: str = f"Отметь свои интересы (минимум {MIN_NO_INTERESTS})"

SUBMIT_TEXT: str = "🚀Подтвердить🚀"

CHECK_TEXT: str = "✅"

NOT_ENOUGH_INTERESTS_TEXT: str = f"Недостаточно интересов (минимум {MIN_NO_INTERESTS})"

NO_BUTTONS_IN_ROW = 2

INTERESTS = [
    'Harry Potter', 'спа-процедуры',
    'джин-тоник', 'медитация',
    'баскетбол', 'хеви-метал',
    'гимнастика', 'азиатская еда',
    'поэзия', 'литература',
    'философия', 'вечеринки',
    'йога', 'хоккей',
    'театр', 'кафе и рестораны',
    'кроссовки', 'животные',
    'Instagram', 'маркетинг и SMM',
    'карты таро', 'оккультизм',
    'бег', 'путешествия',
    'фильмы и сериалы', 'Netflix',
    'Marvel', 'танцы',
    'бани', 'кальян',
    'изучение языков', 'фриланс',
    'скейтбординг', 'K-pop',
    'фотография', 'экстремальный спорт',
    'болливуд', 'яхтинг',
    'пение', 'саморазвитие',
    'спорт', 'диеты',
    'здоровье и медицина', 'стендап-комедия',
    'кофе', 'алкогольные напитки',
    'вязание', 'Fortnite',
    'Minecraft', 'Dota 2',
    'CS go', 'компьютерные игры',
    'душевное здоровье', 'психология',
    'экология', 'активизм',
    'политика', 'Lana Del Ray',
    'мемы', 'права человека',
    'искусство', 'шахматы',
    'бизнес',
    'феминизм',
    'права ЛГБТК',
    'квесты',
    'шоппинг',
    'инвестиции',
    'криптовалюта',
    'большой теннис',
    'теле-шоу',
    'рисование',
    'коньки',
    'создание контента',
    'машины',
    'единоборства',
    'велоспорт',
    'аниме',
    'косплеи',
    'боулинг',
    'конный спорт',
    'мясо',
    'вегетарианство',
    'вино',
    'хиппи-культура',
    'балет',
    'ночные клубы',
    'метавселенная',
    'искусственный интеллект',
    'музыка',
    'экономика',
    'статистика',
    'математика',
    'кулинария',
    'макияж',
    'Twitch',
    'программирование',
    'TikTok',
]


# checked versions
INTERESTS_CHECKED_VERSIONS = [
    CHECK_TEXT + interest + CHECK_TEXT
    for interest in INTERESTS
]


def __get_question_kb_template() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for interest in INTERESTS:
        builder.button(
            text=interest,
            callback_data=CheckInterestCallbackFactory(interest=interest).pack(),
        )

    builder.adjust(NO_BUTTONS_IN_ROW)

    builder.row(
        InlineKeyboardButton(
            text=SUBMIT_TEXT,
            callback_data=SubmitCallbackFactory().pack(),
        )
    )

    return builder.as_markup()


QUESTION_KB_TEMPLATE = __get_question_kb_template()
