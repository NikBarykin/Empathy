from stage import Stage
from command_start import get_id

from user_state import UserState
from stage_order import next_stage

from aiogram import Router, types
from aiogram.types import Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State


class NameStage(Stage):
    state = State()
    name: str = "имя"

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        await Stage.bot.send_message(await get_id(state), "Как тебя зовут?")

    @staticmethod
    def register(router: Router) -> None:
        router.message.register(
            NameStage.process,
            # TODO: remove 32
            F.text.len() <= 32,
            NameStage.state,
        )

        router.message.register(
            NameStage.process_invalid_value,
            NameStage.state,
        )

    @staticmethod
    async def process(
        message: Message,
        state: FSMContext,
    ) -> None:
        await state.update_data(**{NameStage.name: message.text})
        await next_stage(NameStage, state)

    @staticmethod
    async def process_invalid_value(message: types.Message):
        await message.reply("Некорректное значение имени")



async def process_name(
        message: Message,
        state: FSMContext,
        ):
    await state.update_data(name=message.text)

    # age
    await message.answer("Сколько тебе лет?")
    await state.set_state(UserState.age)
