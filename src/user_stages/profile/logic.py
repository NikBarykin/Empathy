from stage import Stage
from engine.user import get_user_by_id_with_session, get_field


async def get_profile_caption(user_id: int) -> str:
    """Form profile caption from user with 'user_id'"""
    async with Stage.async_session() as session:
        user = await get_user_by_id_with_session(user_id, session)
        return (f"{user.name}, {user.age}\n"
                f"{user.bio}")


async def get_profile_photo(user_id: int) -> str:
    return await get_field(user_id, "photo")
