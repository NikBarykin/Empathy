from typing import Iterable, Type, Callable
from aiogram import Router
from stage import Stage


def make_stage_registrar(stages: Iterable[Type[Stage]]) -> Callable[[Router], None]:
    def registrar(router: Router):
        for stage in stages:
            stage.register(router)
    return registrar
