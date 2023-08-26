"""Logic for match-stage"""
from logging import Logger

from stages.stage import Stage
from db.user import User

from engine.user import get_user_by_id
from engine.rating import check_mutual_sympathy

from .constants import get_match_text
from .keyboard import get_query_kb


async def send_partner(actor_id: int, partner: User):
    kb = await get_query_kb(
        actor_id=actod_id,
        target_id=partner.id,
        # TODO:
        partner_score=1,
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
    owner: User = await get_user_by_id(id=profile_owner_id)
    await Stage.bot.send_photo(
        char_id=profile_receiver_id,
        photo=owner.photo,
        caption=get_match_text(owner.id),
        parse_mode="MarkdownV2",
    )


async def check_and_process_mutual_sympathy(
    id1: int,
    id2: int,
    logger: Logger,
) -> None:
    if await check_mutual_sympathy(id1, id2):
        logger.info(
            "Mutual sympathy between %s and %s", id1, id2)
        await send_match_profile(id1, id2)
        await send_match_profile(id2, id1)
