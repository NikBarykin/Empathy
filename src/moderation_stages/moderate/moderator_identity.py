from logging import Logger

from dataclasses import dataclass

from aiogram.types import Message


@dataclass
class ModeratorIdentity:
    token: str
    id: int

    def get_pass_text(self) -> str:
        return f"/moderate_{self.token}"

    def check_if_message_from_moderator(
        self,
        message: Message,
        logger: Logger,
    ) -> bool:
        if not message.text or message.text != self.get_pass_text():
            return False
        user_id = message.from_user.id
        if user_id != self.id:
            # Intruder
            logger.warning(
                "%s tried to start moderating with someone else's token %s", user_id, self.token)
            return False
        return True
