from __future__ import annotations
from typing import Type
from aiogram import Bot, Router
from aiogram.fsm.state import StatesGroup
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class Stage(StatesGroup):
    """Basic class for 'stage' in EmpathyBot"""
    name: str = None
    """Stage's name"""

    # global variables
    bot: Bot = None
    async_session: async_sessionmaker[AsyncSession] = None

    next_stage: Type[Stage] = None

    prev_stage: Type[Stage] = None
    """
        The stage where we got here from,
        states automatically in 'go_stage' call
    """

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        """form for prepare method"""
        raise NotImplementedError("Should be implemented in subclass")

    @staticmethod
    def register(router: Router) -> None:
        """form for register method"""
        raise NotImplementedError("Should be implemented in subclass")
