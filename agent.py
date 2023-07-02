from dataclasses import dataclass, field
from typing import Set


AVAILABLE_GENDERS = ('мужчина', 'женщина')
AVAILABLE_CITIES = ("москва", "санкт-петербург")
RELATIONSHIP_GOALS = ("долгосрочные отношения", "краткосрочные отношения", "просто общение")


@dataclass
class Agent:
    user_id: int
    username: str
    name: str
    age: int
    gender: str
    city: str
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
        return f"{self.user_id};{self.username};{self.name};{self.age};{self.gender};{self.city};{self.picture};{self.min_preferred_age};{self.max_preferred_age};{self.about_yourself}"

    def deserialize(serialized: str):
        user_id, user_name, name, age, gender, city, picture, min_preferred_age, max_preferred_age, about_yourself = serialized.split(';')

        return Agent(
                int(user_id),
                user_name,
                name,
                int(age),
                gender,
                city,
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
            data['picture'],
            data['about_yourself'],
            data['min_preferred_age'],
            data['max_preferred_age'],
            )
