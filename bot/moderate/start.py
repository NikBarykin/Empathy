# import logging
# from stage import Stage

# from aiogram import Router
# from aiogram.types import Message
# from aiogram.fsm.state import default_state
# from aiogram.fsm.context import FSMContext


# class StartModerateStage(Stage):
#     state = default_state
#     name: str = "start moderate"

#     @staticmethod
#     async def prepare(*args, **kwargs) -> None:
#         pass

#     @staticmethod
#     async def process(message: Message, state: FSMContext) -> None:
#         logging.info(f"User ")
#         await message.answer("Вы в режиме модератора")

#     @staticmethod
#     def register(router: Router) -> None:
#         router.register.message(
#         )
