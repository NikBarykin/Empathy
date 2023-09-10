"""Logic for match-stage"""
from logging import Logger

from aiogram.types import Message
from aiogram.methods import SendPhoto
from aiogram.enums.parse_mode import ParseMode

from utils.execute_method import execute_method
from database.user import User

from engine.user import get_user_by_id
from engine.rating import check_mutual_sympathy
from engine.score_partner import score_partner

from user_stages.profile.send import send_profile

from .constants import get_match_text
from .keyboard import get_query_kb


async def send_partner(
    actor_id: int,
    partner_id: int,
    logger: Logger | None = None,
) -> Message | None:
    """Return None if something went wrong"""
    kb = await get_query_kb(
        actor_id=actor_id,
        target_id=partner_id,
        partner_score=await score_partner(
            actor_id=actor_id, partner_id=partner_id),
    )
    return await send_profile(
        chat_id=actor_id,
        user_id=partner_id,
        reply_markup=kb,
        logger=logger,
    )


async def send_match_profile(
    profile_owner_id: int,
    profile_receiver_id: int
) -> Message:
    """Send a notification that match happened. Return message with notification."""
    owner: User = await get_user_by_id(id=profile_owner_id)
    return await execute_method(
        SendPhoto(
            chat_id=profile_receiver_id,
            photo=owner.photo,
            caption=get_match_text(owner.id, owner.name),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    )


async def check_and_process_mutual_sympathy(
    id1: int,
    id2: int,
    logger: Logger,
) -> None:
    """
        Check if there is a mutual sympathy between id1 and id2
        and perform further operation if there is.
    """
    if await check_mutual_sympathy(id1, id2):
        logger.info(
            "Mutual sympathy between %s and %s", id1, id2)
        await send_match_profile(id1, id2)
        await send_match_profile(id2, id1)
