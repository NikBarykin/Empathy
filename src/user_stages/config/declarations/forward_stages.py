from typing import Type

from stage import Stage

from user_stages.name.stage import make_name_stage
from user_stages.age.stage import make_age_stage
from user_stages.sex.stage import make_sex_stage
from user_stages.city.stage import make_city_stage
from user_stages.photo.stage import make_photo_stage
from user_stages.interests.stage import make_interests_stage


def make_forward_stage(stage_maker, stage_name_arg: str) -> Type[Stage]:
    # we skip forward stage if target field is already filled
    return stage_maker(stage_name_arg=stage_name_arg, skip_if_field_presented=True)


NameStage = make_forward_stage(make_name_stage, "Имя")
AgeStage = make_forward_stage(make_age_stage, "Возраст")
SexStage = make_forward_stage(make_sex_stage, "Пол")
CityStage = make_forward_stage(make_city_stage, "Город")
PhotoStage = make_forward_stage(make_photo_stage, "Фотография")
InterestsStage = make_forward_stage(make_interests_stage, "Интересы")


FORWARD_STAGES = [
    NameStage,
    SexStage,
    AgeStage,
    CityStage,
    PhotoStage,
    InterestsStage,
]
