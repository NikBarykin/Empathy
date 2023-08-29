from typing import Type

from stage import Stage

from user_stages.name.stage import make_name_stage
from user_stages.age.stage import make_age_stage
from user_stages.sex.stage import make_sex_stage
from user_stages.city.stage import make_city_stage
from user_stages.photo.stage import make_photo_stage
from user_stages.interests.stage import make_interests_stage


NameStage = make_name_stage("Имя")
AgeStage = make_age_stage("Возраст")
SexStage = make_sex_stage("Пол")
CityStage = make_city_stage("Город")
PhotoStage = make_photo_stage("Фотография")
InterestsStage = make_interests_stage("Интересы")


FORWARD_STAGES = [
    NameStage,
    SexStage,
    AgeStage,
    CityStage,
    PhotoStage,
    InterestsStage,
]
