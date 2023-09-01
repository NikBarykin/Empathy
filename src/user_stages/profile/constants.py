"""Constants for profile-stage: button texts and others"""
from database.user import User


def get_profile_caption(user: User) -> str:
    """Form profile caption from user-object"""
    return (f"{user.name}, {user.age}\n"
            f"{user.bio or ''}")


# TODO: smily
UPDATE_BUTTON_TEXT: str = "🎁Обновить анкету🎁"
FREEZE_BUTTON_TEXT: str = "❄️Заморозить анкету❄️"

CONTINUE_TEXT: str = "продолжить"
"""Text in button, that user presses to continue to match-stage"""
