from __future__ import annotations
from typing import Type
from aiogram import Bot, Router, Dispatcher
from aiogram.fsm.state import StatesGroup
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class Stage(StatesGroup):
    """
        Basic class for 'stage' in EmpathyBot.

        Stage is and identity that accumulates
        aiogram-fsm-states, static update-processors (handlers),
        prepare-method and register-method.

        For example there can be ProfileStage that sends user's profile to him,
        waits for his action and processes it (for example freezes his profile).

        NOTE that stages are represented BY CLASSES NOT OBJECTS.
    """
    name: str = None
    """Stage's name, EVERY stage should have a UNIQUE name"""

    # global variables
    bot: Bot = None
    async_session: async_sessionmaker[AsyncSession] = None
    dp: Dispatcher = None

    next_stage: Type[Stage] = None
    prev_stage: Type[Stage] = None

    @staticmethod
    async def prepare(state: FSMContext, *args, **kwargs) -> None:
        """
            Do some preparations for the stage.
            For example send a question-message to user
            like "What is your name?" and then wait for the answer.

            Can have additional helper-arguments.
        """
        raise NotImplementedError("Should be implemented in subclass")

    @staticmethod
    def register(router: Router) -> None:
        """Register update-processors"""
        raise NotImplementedError("Should be implemented in subclass")
