from stages.regular_workflow.name import make_name_stage
from stages.regular_workflow.age import make_age_stage
from stages.regular_workflow.sex import make_sex_stage
from stages.regular_workflow.city import make_city_stage
from stages.regular_workflow.photo import make_photo_stage
from stages.regular_workflow.interests import make_interests_stage


NameStage = make_name_stage(stage_name_arg="Имя")
AgeStage = make_age_stage(stage_name_arg="Возраст")
SexStage = make_sex_stage(stage_name_arg="Пол")
CityStage = make_city_stage(stage_name_arg="Город")
PhotoStage = make_photo_stage(stage_name_arg="Фотография")
InterestsStage = make_interests_stage(stage_name_arg="Интересы")


FORWARD_STAGES = [
    NameStage,
    AgeStage,
    SexStage,
    CityStage,
    PhotoStage,
    InterestsStage,
]
