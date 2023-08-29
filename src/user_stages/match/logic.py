"""Logic for match-stage"""
from logging import Logger

from stage import Stage
from database.user import User

from engine.user import get_user_by_id
from engine.rating import check_mutual_sympathy
from engine.score import score_partner

from user_stages.profile.send import send_profile

from .constants import get_match_text
from .keyboard import get_query_kb


async def send_partner(actor_id: int, partner: User):
    kb = await get_query_kb(
        actor_id=actor_id,
        target_id=partner.id,
        partner_score=await score_partner(
            actor_id=actor_id, partner_id=partner.id),
    )
    return await send_profile(
        chat_id=actor_id,
        user=partner,
        reply_markup=kb,
    )


async def send_match_profile(
    profile_owner_id: int,
    profile_receiver_id: int
) -> None:
    """Send a notification that match happened"""
    owner: User = await get_user_by_id(id=profile_owner_id)
    await Stage.bot.send_photo(
        chat_id=profile_receiver_id,
        photo=owner.photo,
        caption=get_match_text(owner.id, owner.name),
        parse_mode="MarkdownV2",
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
