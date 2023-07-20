from stage import Stage


class OverwriteStageBase(Stage):
    @staticmethod
    def get_stage_mapper() -> StageMapper:
        raise NotImplementedError("Should be implemented in subclass")

    @staticmethod
    def get_state():
        raise NotImplementedError("Should be implemented in subclass")

    @staticmethod
    async def prepare():
        Stage.bot.send_message(user_id, "Какую стадию изменить")

    @staticmethod
    async def process(
        message: Message,
        state: FSMContext,
    ) -> None:
        stage_mapper: StageMapper = get_stage_mapper()
        target_stage: StageType = stage_mapper[message.text]
        await AccomplishmentManager.mark_uncompleted(target_stage, state)
        await target_stage.prepare(
            message.from_user.id, state
        )

    @staticmethod
    async def process_invalid_value(message: Message) -> None:
        message.answer("Неизвестная позиция")

    @staticmethod
    def register(router: Router):
        router.message.register(
            OverwriteStageBase.process,
            F.text.in_(get_stage_mapper.keys())
            get_state(),
        )

        router.message.register(
            OverwriteStageBase.process_invalid_value,
            get_state().
        )
