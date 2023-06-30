from aiogram.fsm.state import State, StatesGroup

class AgentState(StatesGroup):
    age = State()
    gender = State()
    picture = State()
    registered = State()
    rates = State()
