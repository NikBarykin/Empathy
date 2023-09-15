from aiogram.enums.parse_mode import ParseMode


COMMAND_DESCRIPTION: str = "Перезагрузить бота"
"""Description that user sees in telegram-menu"""

USER_HAS_PRIVATE_FORWARDS_TEXT: str = """Чтобы бот работал правильно\\, нужно разрешить ему пересылку сообщений\\:
`Настройки \\(Settings\\) \\-\\> Конфиденциальность \\(Privacy and Security\\) \\-\\> Пересылка сообщений \\(Forwarded Messages\\) \\-\\> Всегда разрешать \\(Always allow\\)` и добавить бота в список исключений \\(возможно, придется подождать несколько секунд пока обновление вступит в силу\\)\\.
Без этого бот не сможет отправить ссылку на твой аккаунт\\, когда случится взаимный лайк\\."""
USER_HAS_PRIVATE_FORWARDS_PARSE_MODE = ParseMode.MARKDOWN_V2
