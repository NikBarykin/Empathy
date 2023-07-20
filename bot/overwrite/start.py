from stage import Stage
from .personal import OverwritePersonalStage
from .preference import OverwritePreferenceState


class OverwriteStartStage(Stage):
    @staticmethod
    async def prepare(
        user_id: int,
        state: FSMContext,
    ) -> None:
        await Stage.bot.send_message(user_id, "personal/preference?")
        await message.and
        # TODO: delete prev message

    @staticmethod
    async def process_personal(
        message: Message,
        state: FSMContext,
    ) -> None:
        await OverwritePersonalStage.prepare(message.from_user.id, state)

    @staticmethod
    def register(router) -> None:
        router.message.register(
            OverwriteStartStage.process_personal,
            F.text.in_()
