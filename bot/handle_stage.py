from stage import Stage


class HandleStage(Stage):
    state = State()
    name: str = "handle stage"

    @staticmethod
    async def prepare(state: FSMContext) -> None:
        await state.update_data(**{HandleStage.name: })
