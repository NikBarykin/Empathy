from stages.regular_workflow.name import make_name_stage
from stages.regular_workflow.age import make_age_stage
from stages.regular_workflow.city import make_city_stage
from stages.regular_workflow.photo import make_photo_stage
from stages.regular_workflow.interests import make_interests_stage


UpdateNameStage = make_name_stage(stage_name_arg="UpdateName")
UpdateAgeStage = make_age_stage(stage_name_arg="UpdateAge")
UpdateCityStage = make_city_stage(stage_name_arg="UpdateCity")
UpdatePhotoStage = make_photo_stage(stage_name_arg="UpdatePhoto")
UpdateInterestsStage = make_interests_stage(stage_name_arg="UpdateInterests")


assert UpdateNameStage.name is not None
assert UpdateAgeStage.name is not None
assert UpdateCityStage.name is not None
assert UpdatePhotoStage.name is not None
assert UpdateInterestsStage.name is not None


UPDATE_STAGES = [
    UpdateNameStage,
    UpdateAgeStage,
    UpdateCityStage,
    UpdatePhotoStage,
    UpdateInterestsStage,
    # TODO:
    # SelfDescriptionStage,
    # RelationshipGoalStage,
    # MinPartnerAgeStage,
    # MaxPartnerAgeStage,
]
