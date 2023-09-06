"""Every helpful function about Rating-model"""
import logging
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from stage import Stage
from database.rating import Rating


async def check_liked(actor_id: int, target_id: int) -> bool:
    """Check if 'actor' liked 'target'"""
    stmt = (
        select(Rating)
        .where(Rating.liked==True)
        .where(Rating.actor_id==actor_id)
        .where(Rating.target_id==target_id)
    )
    async with Stage.async_session() as session:
        result = await session.execute(stmt)
        return result.first() is not None


async def check_mutual_sympathy(user_id1: int, user_id2: int) -> bool:
    """Check whether first user liked second and vice versa"""
    return (
        await check_liked(user_id1, user_id2)
        and
        await check_liked(user_id2, user_id1)
    )


async def submit_rating(
    rating: Rating,
    logger: logging.Logger | None = None
) -> None:
    """Inserts rating into database"""
    try:
        async with Stage.async_session() as session:
            async with session.begin():
                session.add(rating)
        if logger is not None:
            logger.info(
                "Successfully submitted rating %s", rating)
    except IntegrityError as e:
        if logger is not None:
            logger.error(e)
