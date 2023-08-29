"""
    When there is a lack of candidates a user gets into waiting pool.
    And when someone eligible appears, user's in waiting pool get notified
"""
from logging import Logger

from sqlalchemy import select


from database.user import User

from engine.user import (
    get_user_by_id_with_session, update_field, get_user_by_id)
from engine.eligibility import partner_eligibility_expr

from stage import Stage
from .logic import send_partner

# TODO: Bad situation: user is overwriting something and gets notified


async def notify_waiting_pool(new_user_id: int, logger: Logger) -> None:
    """Notify user's from waiting pool, who can be interested in new user"""
    async with Stage.async_session() as session:
        new_user: User = await get_user_by_id_with_session(
            new_user_id, session=session)

        stmt = (
            select(User.id)
            .where(User.in_waiting_pool)
            .where(~User.frozen)
            .where(partner_eligibility_expr(actor=User, target=new_user))
        )

        target_ids = (await session.scalars(stmt)).all()

    for target_id in target_ids:
        target: User = await get_user_by_id(target_id)
        if not target.in_waiting_pool:
            logger.debug(
                "%s was already notified, so there is no need to notify him again", target)
            continue

        await put_in_waiting_pool(target_id, logger=logger)

        await send_partner(actor_id=target_id, partner=new_user)

        logger.debug("%s was notified about %s", target, new_user)


async def put_in_waiting_pool(actor_id: int, logger: Logger):
    """Move user to 'waiting' status"""
    result = await update_field(
        id=actor_id,
        field_name="in_waiting_pool",
        value=True,
    )
    logger.debug("%s was put into waiting pool", actor_id)
    return result


async def remove_from_waiting_pool(actor_id: int, logger: Logger):
    """Mark user as removed from waiting pool"""
    result = await update_field(
        id=actor_id,
        field_name="in_waiting_pool",
        value=False,
    )
    logger.debug("%s was removed from waiting_pool", actor_id)
    return result
