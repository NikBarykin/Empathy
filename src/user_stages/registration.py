from logging import Logger

from aiogram.fsm.context import FSMContext

from utils.id import get_id
from utils.logger import create_logger

from stage import Stage, go_next_stage

from user_stages.match.waiting_pool import notify_waiting_pool


class RegistrationStage(Stage):
    """
        Actions that should be done on new user registration,
        for example, some user's in waiting pool should be notified
    """
    name: str = "RegistrationStage"
    __logger: Logger = create_logger(stage_name=name)

    @staticmethod
    async def prepare(state: FSMContext):
        result = await go_next_stage(
            departure=RegistrationStage,
            state=state,
        )
        await notify_waiting_pool(
            new_user_id=await get_id(state), logger=RegistrationStage.__logger)
        return result

    @staticmethod
    def register(*args, **kwargs) -> None:
        """No handles to register, only 'prepare' method"""
