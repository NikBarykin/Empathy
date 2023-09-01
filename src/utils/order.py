from typing import Type, Callable, Awaitable

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from stage import Stage


def connect_bydir(departure: Type[Stage], destination: Type[Stage]):
    """Connect in both directions"""
    departure.next_stage = destination
    destination.prev_stage = departure


def make_stage_jumper(
    target_stage: Type[Stage],
) -> Callable[[Message, FSMContext], Awaitable[Message]]:
    """Creates a stage-jumper that proceeds to target_stage"""
    async def stage_jumper(_: Message, state: FSMContext) -> Message:
        """Handles an event, ignores it and prepares target stage"""
        return await target_stage.prepare(state)
    return stage_jumper
