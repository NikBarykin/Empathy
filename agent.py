from dataclasses import dataclass, field
from typing import Set

# from gender import Gender


@dataclass
class Agent:
    user_id: int
    user_name: str
    age: int
    gender: str
    picture: str
    like_ids: Set[int] = field(default_factory=lambda: set())
    dislike_ids: Set[int] = field(default_factory=lambda: set())

    def rate(self, other) -> int:
        if other.user_id == self.user_id or other.gender == self.gender:
            return -1 # we don't want to date ourself or someone with the same gender

        return 6 - abs(self.age - other.age)

    def serialize(self) -> str:
        return f"{self.user_id} {self.user_name} {self.age} {self.gender} {self.picture}"

    def deserialize(serialized: str):
        user_id, user_name, age, gender, picture = serialized.split()
        return Agent(int(user_id), user_name, int(age), gender, picture)
