from logging import Logger
from typing import Optional

from aiogram import Bot, Router, types
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from sqlalchemy import select

from stage import Stage

from database.user import User

from engine.user import submit_user

from utils.logger import create_logger

from .logic import skip_completed_field_stages


class StartStage(Stage):
    name: int = "start stage"
    description: str = "Перезагрузить бота"
    # __process_state = State(state="process_" + name)
    __logger: Logger = create_logger(name)

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        pass

    @staticmethod
    async def skip_completed_field_stages(state: FSMContext) -> None:


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
        await state.set_data({id: user_id})

        StartStage.__logger.info(
            "%s started successfully", user_id)

        return await skip_completed_field_stages(state)

    @staticmethod
    def register(router: Router) -> None:
        router.message.register(
            StartStage.process,
            Command("start"),
            # default_state,
            # StartStage.state,
        )
