import logging

from aiogram import Bot, Router
from aiogram.fsm.state import StatesGroup
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from typing import Type


class Stage(StatesGroup):
    """Basic class for 'stage' in EmpathyBot"""
    name: str = None

    bot: Bot = None
    async_session: async_sessionmaker[AsyncSession] = None

    next_stage = None

    prev_stage = None
    """
        The stage where we got here from,
        states automatically in 'go_stage' call
    """

#     # this attribute is common for every stage
#     # because it has to be specified in 'order-section' and not in some 'stage-section'
#     allow_go_back: bool = True

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        """form for prepare method"""
        raise NotImplementedError("Should be implemented in subclass")

    @staticmethod
    def register(router: Router) -> None:
        """form for register method"""
        raise NotImplementedError("Should be implemented in subclass")


# TODO: get reed of this function
async def go_stage(
    departure: Type[Stage],
    destination: Type[Stage],
    state: FSMContext,
):
    return await destination.prepare(state)


async def go_next_stage(
    departure: Type[Stage],
    state: FSMContext,
):
    return await go_stage(
        departure=departure,
        destination=departure.next_stage,
        state=state,
    )


# def forbid_go_back(stage: Type[Stage]) -> None:
#     stage.allow_go_back = False
