from logging import Logger

from engine.user import update_field


async def __update_freeze_field(
    user_id: int,
    new_value: bool,
):
    return await update_field(
        id=user_id,
        field_name="frozen",
        value=new_value,
    )


async def freeze_user(user_id: int, logger: Logger | None):
    result = await __update_freeze_field(user_id, True)
    logger.debug("User %s was frozen successfully", user_id)
    return result


async def unfreeze_user(user_id: int, logger: Logger | None):
    result = await __update_freeze_field(user_id, False)
    logger.debug("User %s was unfrozen successfully", user_id)
    return result
