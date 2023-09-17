import os

ADD_PROFILE_PHOTO_TEXT = "Добавить фотографию из профиля"
PREPARE_TEXT: str = "Добавь фотографию"
"""Text of a message that is shown first when photo-stage is being prepared"""
PROFILE_PHOTO_DIR: str = "profile_photos"


def get_profile_photo_path(photo_file_name: str):
    return os.path.join(PROFILE_PHOTO_DIR, photo_file_name)
