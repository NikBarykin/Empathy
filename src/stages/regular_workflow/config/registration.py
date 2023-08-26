from .declarations.all_stages import ALL_STAGES
from aiogram import Router


def register_stages(router: Router) -> None:
    for stage in ALL_STAGES:
        stage.register(router)
