"""Constants for profile-stage: button texts and others"""
from db.user import User


def get_profile_caption(user: User) -> str:
    """Form profile caption from user-object"""
    return (f"{user.name}, {user.age}\n"
            f"{user.self_description or ''}")


# TODO: smily
UPDATE_BUTTON_TEXT: str = "🎁Обновить анкету🎁"
FREEZE_BUTTON_TEXT: str = "❄️Заморозить анкету❄️"
