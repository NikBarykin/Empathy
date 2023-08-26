"""Constants for match-stage"""
LIKE_TEXT: str = "👍"
DISLIKE_TEXT: str = "👎"
PARTNERS_NOT_FOUND_TEXT: str = (
    "На данный момент партнеров не найдено. "
    "Когда появятся подходящие варианты, мы обязательно тебе напишем!😉"
)


def get_match_text(partner_id: int) -> str:
    """Create a text, that is printed, when mutual sympathy happens"""
    return (f"🔥У вас взаимная симпатия с "
            f"[пользователем](tg://user?id={partner_id})🔥")
