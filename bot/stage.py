from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from aiogram.fsm.state import StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot
from typing import List, Type


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



    # @staticmethod
    # async def next(
    #     stage: StageType,
    #     user_id: int,
    #     state: FSMContext,
    # ) -> None:
    #     next_stage: Stage = stage.next_stage
    #     if next_stage is not None:
    #         await state.set_state(next_stage.state)
    #         await next_stage.prepare(user_id, state)

    # @staticmethod
    # def initialize(
    #     bot: Bot,
    #     router: Router,
    #     start_stage: StageType,
    #     personal_stages: List[StageType],
    #     match_stage: StageType,
    #     overwrite_stages: List[StageType],
    # ) -> None:
    #     Stage.bot = bot

    #     Stage.start_stage = start_stage
    #     Stage.personal_stages = { stage.name: stage for stage in personal_stages }
    #     Stage.preference_stages = { stage.name: stage for stage in preference_stages }
    #     Stage.match_stages = match_stages

    #     all_stages = (
    #         [start_stage] + personal_stages + preference_stages + match_stages
    #     )

    #     Stage.mark_uncompleted_stages(all_stages)
    #     Stage.register_stages(all_stages, router)



    # @staticmethod
    # def overwrite_stage():


    # @staticmethod
    # def chain_stages(stages: List[Type[Stage]]) -> None:
    #     """
    #     The last stage chains to itself
    #     """
    #     for i in range(len(stages)):
    #         next_stage_i: int = i + int(i + 1 < len(stages))
    #         stages[i].next_stage = stages[next_stage_i]

    # @staticmethod
    # def register_stages(stages: List[StageType], router: Router) -> None:
    #     for stage in stages:
    #         stage.register(router)

StageType = Type[Stage]
