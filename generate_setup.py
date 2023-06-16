import random
from agent import Agent

MALE_NAMES = ["Ivan", "Oleg", "Alexei", "Maksim", "Egor"]
FEMALE_NAMES = ["Masha", "Sasha", "Dunya", "Tatiana", "Olga"]

MIN_AGE = 18
MAX_AGE = 30

NAMES = MALE_NAMES + FEMALE_NAMES

NO_AGENTS = 50

lines = []

for i in range (NO_AGENTS):
    name = random.choice(NAMES)
    age = random.randint(MIN_AGE, MAX_AGE)
    gender = "Male" if name in MALE_NAMES else "Female"

    agent = Agent(i, name, age, gender)
    lines.append(agent.serialize())

with open("setup.txt", "w") as f:
    f.writelines('\n'.join(lines))
