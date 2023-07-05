from dataclasses import dataclass, field
from typing import Set


AVAILABLE_GENDERS = ('мужчина', 'женщина')
AVAILABLE_CITIES = ("москва", "санкт-петербург")
RELATIONSHIP_GOALS = ("долгосрочные отношения", "краткосрочные отношения", "просто общение")
INTERESTS = ("спорт", "наука", "искусство")


@dataclass(unsafe_hash=True, frozen=True)
class Agent:
    user_id: int
    username: str
    name: str
    age: int
    gender: str
    city: str
    relationship_goal: str
    picture: str
    about_yourself: str

    min_preferred_age: int
    max_preferred_age: int

    liked_ids: Set[int] = field(default_factory=lambda: set())
    disliked_ids: Set[int] = field(default_factory=lambda: set())

    # def rate(self, other) -> int:
    #     if other.user_id == self.user_id or other.gender == self.gender:
    #         return -1 # we don't want to date ourself or someone with the same gender

    #     return 6 - abs(self.age - other.age)

    def serialize(self) -> str:
        return ';'.join(
                map(
                    str,
                    [
                        self.user_id,
                        self.username,
                        self.name,
                        self.age,
                        self.gender,
                        self.city,
                        self.relationship_goal,
                        self.picture,
                        self.about_yourself
                        self.min_preferred_age,
                        self.max_preferred_age,
                        ]
                    )
                )

    def deserialize(serialized: str):
        (

                user_id,
                username,
                name,
                age,
                gender,
                city,
                relationship_goal,
                picture,
                about_yourself
                min_preferred_age,
                max_preferred_age,
                = 
                serialized.split(';')
                )

        return Agent(
                int(user_id),
                user_name,
                name,
                int(age),
                gender,
                city,
                relationship_goal,
                picture,
                about_yourself,
                int(min_preferred_age),
                int(max_preferred_age),
                )

def create_agent(data) -> Agent:
    return Agent(
            data['user_id'],
            data['username'],
            data['name'],
            data['age'],
            data['gender'],
            data['city'],
            data['relationship_goal'],
            data['picture'],
            data['about_yourself'],
            data['min_preferred_age'],
            data['max_preferred_age'],
            )
