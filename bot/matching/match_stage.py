from aiogram.types import Message
from stage import Stage

class MatchStage(Stage):
    state = State()

    @staticmethod
    async def prepare():
        pass

    async def process_overwrite(
        message: Message,
        state: FSMContext,
    ) -> None:
        await OverwriteStage.prepare()


    async def process_choose_overwrite_type(
        message: Message) -> None:

        if message.text == "personal":
        elif message.text == "preference":

        else:
            unknown




    @staticmethod
    def register():
        pass
