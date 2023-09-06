from stage import Stage


async def get_bio_from_telegram(user_id: int) -> str | None:
    """Get bio section from user's telegram account"""
    user_info = await Stage.bot.get_chat(user_id)
    return user_info.bio
