from stage import Stage

from matching.stage import insert_rating

from db.user import User


async def test_main():
    user1 = User(id=123456
