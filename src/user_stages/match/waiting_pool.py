"""
    When there is a lack of candidates a user gets into waiting pool.
    And when someone eligible appears, user's in waiting pool get notified
"""
from logging import Logger

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sqlalchemy import select

from database.user import User

from engine.user import (
    get_user_by_id_with_session, get_user_by_id)
from expressions.eligibility import relationship_eligibility_expr
from expressions.rated import rated_expr

from utils.state import get_state_by_id

from stage import Stage

from .waiting_pool_utils import remove_from_waiting_pool

from .stage import MatchStage


async def notify_user_about_partner(
    actor_id: int,
    partner_id: int,
    logger: Logger,
) -> Message | None:
    """
        Notify 'actor_id' about appearance of 'partner_id'.
        Effectively call MatchStage.prepare.
        If everything is OK return notification-message.
    """
    result = await MatchStage.prepare(
        state=get_state_by_id(actor_id),
        target_id=partner_id,
    )

    logger.debug("%s was notified about %s", actor_id, partner_id)

    return result


async def notify_waiting_pool(new_user_id: int, logger: Logger) -> None:
    """Notify user's from waiting pool, who can be interested in new user"""
    async with Stage.async_session() as session:
        new_user: User = await get_user_by_id_with_session(
            new_user_id, session=session)

        stmt = (
            select(User.id)
            .where(User.in_waiting_pool)
            .where(~rated_expr(actor=User, target=new_user))
            .where(relationship_eligibility_expr(User, new_user))
        )

        target_ids = (await session.scalars(stmt)).all()

    for target_id in target_ids:
        target: User = await get_user_by_id(target_id)
        if not target.in_waiting_pool:
            logger.debug(
                "%s was already notified, so there is no need to notify him again", target)
            continue

        await remove_from_waiting_pool(target_id, logger=logger)

        await notify_user_about_partner(
            actor_id=target_id, partner_id=new_user.id, logger=logger)
