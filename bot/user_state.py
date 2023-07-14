from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    # form
    name = State()
    age = State()
    sex = State()
    city = State()
    relationship_goal = State()
    interests = State()
    photo = State()
    self_description = State()
    # preferences
    min_preferred_age = State()
    max_preferred_age = State()
    preferred_partner_interests = State()
    # match
    registered = State()
    # rates = State()
