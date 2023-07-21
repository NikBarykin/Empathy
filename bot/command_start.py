from stage import Stage
from stage_order import next_stage
from aiogram import Bot, Router, types
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from aiogram.fsm.state import default_state

# import registration_end
# from db.user import User

router = Router()

# async def user_already_in_database(
#         telegram_id: int,
#         async_session: async_sessionmaker[AsyncSession],
#         ) -> bool:
#     async with async_session() as session:
#         stmt = select(User.id).where(User.id == telegram_id)
#         result = await session.execute(stmt)
#         return result.scalars().first() is not None


class StartStage(Stage):
    state = default_state
    name: int = "start stage"
    id_key: int = "id"
    handle_key: int = "handle"


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
        await state.update_data(**{
            StartStage.id_key: message.from_user.id,
            StartStage.handle_key: message.from_user.username,
        })
        await next_stage(StartStage, state)


async def get_id(state: FSMContext) -> int:
    return (await state.get_data())[StartStage.id_key]


async def get_handle(state: FSMContext) -> str:
    return (await state.get_data())[StartStage.handle_key]



# @router.message(Command('start'))
# async def process_command_start(
#     message: types.Message,
#     bot: Bot,
#     state: FSMContext,
#     async_session: async_sessionmaker[AsyncSession],
# ):
#     telegram_id = message.from_user.id

#     # TODO: better answers
#     if await user_already_in_database(telegram_id, async_session):
#         await registration_end.process_end(
#                 bot,
#                 message.from_user.id,
#                 state,
#                 async_session,
#                 )

#     else:
#         await state.update_data(telegram_id=telegram_id)
#         await state.update_data(telegram_handle=message.from_user.username)

#         await message.answer("Как тебя зовут?")
#         await state.set_state(UserState.name)
