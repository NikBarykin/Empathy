from database.user import MAX_BIO_SZ


TARGET_FIELD_NAME: str = "bio"
QUESTION_TEXT: str = "Напиши небольшое описание к своей анкете"
"""Text, that asks user to fill bio field"""
INVALID_VALUE_TEXT: str = f"Слишком длинное описание: максимальный размер {MAX_BIO_SZ} символов"
"""Text that shows when user enters too long bio"""
