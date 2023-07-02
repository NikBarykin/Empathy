from aiogram.fsm.state import State, StatesGroup

class AgentState(StatesGroup):
    # form
    name = State()
    age = State()
    gender = State()
    city = State()
    relationship_goal = State()
    picture = State()
    about_yourself = State()
    # preferences
    min_preferred_age = State()
    max_preferred_age = State()
    # match
    registered = State()
    rates = State()
