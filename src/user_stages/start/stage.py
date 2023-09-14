from logging import Logger
from typing import Type

from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage

from stage import Stage

from database.user import User

from engine.user import submit_user, reset_metadata

from utils.logger import create_logger
from utils.restart_state import restart_state
from utils.execute_method import execute_method

from user_stages.field_stages.base import FieldStageBase

from .constants import (
    COMMAND_DESCRIPTION,
    USER_HAS_PRIVATE_FORWARDS_TEXT,
    USER_HAS_PRIVATE_FORWARDS_PARSE_MODE,
)
from .logic import user_has_private_forwards


class StartStage(Stage):
    name: int = "start"
    description: str = COMMAND_DESCRIPTION
    # __process_state = State(state="process_" + name)
    __logger: Logger = create_logger(name)

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        pass

    @staticmethod
    async def __find_first_uncompleted_stage(state: FSMContext):
        result: Type[Stage] = StartStage.next_stage
        while issubclass(result, FieldStageBase) and await result.check_field_already_presented(state):
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
    ):
        """
            Restarts bot, clears aiogram-state,
            updates some metadata in database, BUT doesn't remove user from database.
            Skips stages that are already presented by user.
            Also check that user doesn't have private forwards.
        """
        user_id = message.from_user.id

        if await user_has_private_forwards(user_id):
            return await execute_method(
                SendMessage(
                    chat_id=user_id,
                    text=USER_HAS_PRIVATE_FORWARDS_TEXT,
                    parse_mode=USER_HAS_PRIVATE_FORWARDS_PARSE_MODE,
                )
            )


        await submit_user(User(id=user_id), logger=StartStage.__logger)
        await reset_metadata(user_id=user_id)

        await restart_state(state=state, user_id=user_id)

        StartStage.__logger.info(
            "%s started successfully", user_id)

        return await StartStage.skip_completed_field_stages(state)

    @staticmethod
    def register(router: Router) -> None:
        # start-command is available from any state
        router.message.register(
            StartStage.process,
            Command(StartStage.name),
        )
