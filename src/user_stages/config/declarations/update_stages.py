from user_stages.name.stage import make_name_stage
from user_stages.sex.stage import make_sex_stage
from user_stages.age.stage import make_age_stage
from user_stages.age.partner_age import (
    make_min_partner_age_stage, make_max_partner_age_stage)
from user_stages.city.stage import make_city_stage
from user_stages.photo.stage import make_photo_stage
from user_stages.interests.stage import make_interests_stage
from user_stages.bio.stage import make_bio_stage


UpdateNameStage = make_name_stage("Обновить имя")
UpdateSexStage = make_sex_stage("Обновить пол")
UpdateAgeStage = make_age_stage("Обновить возраст")
UpdateCityStage = make_city_stage("Обновить город")
UpdatePhotoStage = make_photo_stage("Обновить фото")
UpdateInterestsStage = make_interests_stage("Обновить интересы")
UpdateBioStage = make_bio_stage("О себе")
UpdateMinPartnerAgeStage = make_min_partner_age_stage("Минимальный возраст партнера")
UpdateMaxPartnerAgeStage = make_max_partner_age_stage("Максимальный возраст партнера")


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
    UpdateMinPartnerAgeStage,
    UpdateMaxPartnerAgeStage,
    # TODO:
    # SelfDescriptionStage,
    # RelationshipGoalStage,
    # MinPartnerAgeStage,
    # MaxPartnerAgeStage,
]
