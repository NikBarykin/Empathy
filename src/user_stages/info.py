from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.methods import SendMessage
from aiogram.enums.parse_mode import ParseMode

from stage import Stage

from utils.id import get_id
from utils.execute_method import execute_method


INFO: str = """
***Как работает бот?***
Сначала ты отвечаешь на несколько вопросов\\, а затем бот предлагает тебе анкеты других людей\\, опираясь на твои предпочтения\\. Каждой анкете можно поставить лайк \\(👍\\) либо дизлайк \\(👎\\)\\. Когда у двух пользователей случается взаимный лайк\\, бот присылает обоим аккаунт партнера\\, чтобы продолжить общение в личной переписке\\.

При возникновении какой\\-либо ошибки следует перезагрузить бота командой /start\\. Если после этого ошибка осталась\\, следует написать в [техподдержку](tg://user?id=6434294262)\\.

***Правила***
• Запрещена нецензурная речь в любом виде\\.
• Принимаются только реальные фотографии пользователя без посторонних людей\\.
"""


class InfoStage(Stage):
    name: str = "info"
    description: str = "О боте"

    @staticmethod
    async def prepare(state: FSMContext):
        pass

    @staticmethod
    async def process(message: Message, state: FSMContext):
        """Send info to user"""
        return await execute_method(
            SendMessage(
                chat_id=message.from_user.id,
                text=INFO,
                parse_mode=ParseMode.MARKDOWN_V2,
            )
        )

    @staticmethod
    def register(router: Router):
        router.message.register(
            InfoStage.process,
            Command(InfoStage.name),
        )
