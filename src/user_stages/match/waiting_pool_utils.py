"""Hooks on updating 'in_waiting_pool'-field of user"""
from logging import Logger

from engine.user import update_field


async def put_in_waiting_pool(actor_id: int, logger: Logger) -> None:
    """Move user to 'waiting' status"""
    await update_field(
        id=actor_id,
        field_name="in_waiting_pool",
        value=True,
    )
    logger.debug("%s was put into waiting pool", actor_id)


async def remove_from_waiting_pool(actor_id: int, logger: Logger) -> None:
    """Mark user as removed from waiting pool"""
    await update_field(
        id=actor_id,
        field_name="in_waiting_pool",
        value=False,
    )
    logger.debug("%s was removed from waiting_pool", actor_id)
