from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from aiogram.fsm.state import StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot
from typing import List, Type


# class StageMeta(type(StatesGroup), ABCMeta):
#     pass


# TODO: make abstract
class Stage(StatesGroup):
    StageType = Type[Stage]

    next_stage: Stage = None

    @staticmethod
    # @abstractmethod
    async def prepare(user_id: int, state: FSMContext) -> None:
        pass

    @staticmethod
    # @abstractmethod
    def register(router: Router) -> None:
        pass

    @staticmethod
    def mark_completed(stage: StageType) -> None:
        stage.completed = True

    @staticmethod
    def mark_uncompleted(stage: StageType) -> None:
        stage.completed = False

    @staticmethod
    async def next(
        stage: Type[Stage],
        user_id: int,
        state: FSMContext,
    ) -> None:
        next_stage: Stage = stage.next_stage
        if next_stage is not None:
            await state.set_state(next_stage.state)
            await next_stage.prepare(user_id, state)

    @staticmethod
    def initialize(
        bot: Bot,
        start_stage: StageType,
        personal_stages: List[StageType],
        preference_stages: List[StageType],
        match_stages: List[StageType],
    ) -> None:
        Stage.bot = bot
        Stage.start_stage = start_stage
        Stage.personal_stages = personal_stages
        Stage.preference_stages = preference_stages
        Stage.match_stages = match_stages

    @staticmethod
    def chain_stages(stages: List[Type[Stage]]) -> None:
        """
        The last stage chains to itself
        """
        for i in range(len(stages)):
            next_stage_i: int = i + int(i + 1 < len(stages))
            stages[i].next_stage = stages[next_stage_i]

    @staticmethod
    def register_stages(stages: List[Type[Stage]], router: Router) -> None:
        for stage in stages:
            stage.register(router)

    def
