from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from aiogram.fsm.state import StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot
from typing import List, Type
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


# TODO: make abstract
class Stage(StatesGroup):
    bot = None
    async_session = None
    register_stage = None

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        raise NotImplementedError("Should be implemented in subclass")

    @staticmethod
    def register(router: Router) -> None:
        raise NotImplementedError("Should be implemented in subclass")


StageType = Type[Stage]


class Stage(StatesGroup):
    """Basic stage class"""
    bot: Bot = None
    async_session: async_sessionmaker[AsyncSession] = None

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        """form for prepare method"""
        raise NotImplementedError("Should be implemented in subclass")

    @staticmethod
    def register(router: Router) -> None:
        """form for register method"""
        raise NotImplementedError("Should be implemented in subclass")
