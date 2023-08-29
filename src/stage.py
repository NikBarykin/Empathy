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

    allow_go_back: bool = True

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        """form for prepare method"""
        raise NotImplementedError("Should be implemented in subclass")

    @staticmethod
    def register(router: Router) -> None:
        """form for register method"""
        raise NotImplementedError("Should be implemented in subclass")


async def go_stage(
    departure: Type[Stage],
    destination: Type[Stage],
    state: FSMContext,
):
    # TODO: rework all prev_stage system
    for _  in range(10):
        print(f"departure={departure.name}, destination={destination.name}")
    if destination.prev_stage is None:
        destination.prev_stage = departure
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


# def connect(first_stage: Type[Stage], late_stage: Type[Stage]) -> None:
#     """Connect two consecutive stages"""
#     first_stage.next_stage = late_stage
#     late_stage.prev_stage = first_stage


def forbid_go_back(stage: Type[Stage]) -> None:
    stage.allow_go_back = False
