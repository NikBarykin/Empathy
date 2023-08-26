from logging import Logger
from typing import Optional

from aiogram import Bot, Router, types
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from sqlalchemy import select

from stages.stage import Stage

from db.user import User

from engine.user import submit_user

from utils.logger import create_logger



class StartStage(Stage):
    state = default_state
    name: int = "start stage"
    id_key: int = "id"
    handle_key: int = "handle"
    __logger: Logger = create_logger(name)

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        pass

    @staticmethod
    def register(router: Router) -> None:
        router.message.register(
            StartStage.process,
            Command("start"),
            # default_state,
            # StartStage.state,
        )

    @staticmethod
    async def process(
        message: Message,
        state: FSMContext,
    ) -> None:
        # User doesn't have a username
        if message.from_user.username is None:
            await message.answer(
                "Ошибка: у тебя не настроенно имя пользователя в telegram")
            return

        new_user = User(
            id=message.from_user.id,
            username=message.from_user.username,
        )

        await submit_user(new_user, logger=StartStage.__logger)

        async with Stage.async_session() as session:
            async with session.begin():
                session.add(new_user)

        await state.update_data(
            id=new_user.id,
            name=message.from_user.first_name,
        )

        StartStage.__logger.info(
            "%s started successfully", new_user)

        await StartStage.next_stage.prepare(state)
