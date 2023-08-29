from aiogram import Router
from .declarations.all_stages import ALL_STAGES


def register_user_stages(router: Router) -> None:
    for stage in ALL_STAGES:
        stage.register(router)
