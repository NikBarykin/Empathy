from typing import Type, Callable, Awaitable

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from stage import Stage
from fork_stage.base import ForkStageBase


def connect_bydir(departure: Type[Stage], destination: Type[Stage]) -> None:
    """Connect in both directions"""
    departure.next_stage = destination
    destination.prev_stage = departure


def add_alternative_bydir(fork_stage: Type[ForkStageBase], alternative: Type[Stage]) -> None:
    """Add 'alternative' to fork_stage and set alternative.prev_stage=fork_stage"""
    fork_stage.add_alternative(alternative)
    alternative.prev_stage = fork_stage


def make_stage_jumper(
    target_stage: Type[Stage],
) -> Callable[[Message, FSMContext], Awaitable[Message]]:
    """Creates a stage-jumper that proceeds to target_stage, ignoring message-event"""
    async def stage_jumper(_: Message, state: FSMContext) -> Message:
        """Handles an event, ignores it and prepares target stage"""
        return await target_stage.prepare(state)
    return stage_jumper
