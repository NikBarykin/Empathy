from typing import Type

from stage import Stage

from user_stages.name.stage import make_name_stage
from user_stages.sex.stage import make_sex_stage
from user_stages.age.stage import make_age_stage
from user_stages.city.stage import make_city_stage
from user_stages.photo.stage import make_photo_stage
from user_stages.interests.stage import make_interests_stage
from user_stages.bio.stage import make_bio_stage


def make_update_stage(stage_maker, stage_name_arg: str) -> Type[Stage]:
    # We never skip update-stage
    return stage_maker(stage_name_arg=stage_name_arg, skip_if_field_presented=False)


UpdateNameStage = make_update_stage(make_name_stage, "Обновить имя")
UpdateSexStage = make_update_stage(make_age_stage, "Обновить пол")
UpdateAgeStage = make_update_stage(make_sex_stage, "Обновить возраст")
UpdateCityStage = make_update_stage(make_city_stage, "Обновить город")
UpdatePhotoStage = make_update_stage(make_photo_stage, "Обновить фото")
UpdateInterestsStage = make_update_stage(make_interests_stage, "Обновить интересы")
UpdateBioStage = make_update_stage(make_bio_stage, "О себе")


assert UpdateNameStage.name is not None
assert UpdateAgeStage.name is not None
assert UpdateCityStage.name is not None
assert UpdatePhotoStage.name is not None
assert UpdateInterestsStage.name is not None


UPDATE_STAGES = [
    UpdateNameStage,
    UpdateSexStage,
    UpdateAgeStage,
    UpdateCityStage,
    UpdatePhotoStage,
    UpdateInterestsStage,
    UpdateBioStage,
    # TODO:
    # SelfDescriptionStage,
    # RelationshipGoalStage,
    # MinPartnerAgeStage,
    # MaxPartnerAgeStage,
]
