from logging import Logger
from typing import Optional

from aiogram import Bot, Router, types
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from sqlalchemy import select

from stage import Stage, go_stage

from database.user import User

from engine.user import submit_user

from utils.logger import create_logger

from user_stages.config.declarations.forward_stages import FORWARD_STAGES

from .constants import COMMAND_DESCRIPTION


class StartStage(Stage):
    name: int = "StartStage"
    description: str = COMMAND_DESCRIPTION
    # __process_state = State(state="process_" + name)
    __logger: Logger = create_logger(name)

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        pass

    @staticmethod
    async def __find_first_uncompleted_stage(state: FSMContext):
        result = StartStage.next_stage
        while result in FORWARD_STAGES and await result.check_field_already_presented(state):
            result = result.next_stage
        return result

    @staticmethod
    async def skip_completed_field_stages(state: FSMContext):
        """Skip forward stages that are already completed (fields are filled in database)"""
        following_stage = await StartStage.__find_first_uncompleted_stage(state)
        return await following_stage.prepare(state)

    @staticmethod
    async def process(
        message: Message,
        state: FSMContext,
    ) -> None:
        """
            Restarts bot, clears aiogram-state, BUT doesn't remove user from database.
            Skips stages that are already presented by user
        """
        # TODO: process_state
        user_id = message.from_user.id
        await submit_user(User(id=user_id), logger=StartStage.__logger)

        await state.clear()
        await state.set_data({"id": user_id})

        StartStage.__logger.info(
            "%s started successfully", user_id)

        return await StartStage.skip_completed_field_stages(state)

    @staticmethod
    def register(router: Router) -> None:
        router.message.register(
            StartStage.process,
            Command("start"),
            # default_state,
            # StartStage.state,
        )
