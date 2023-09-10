"""Import this module to create user-stages and order them"""
from utils.order import connect_bydir, add_alternative_bydir

from user_stages.start import StartStage

# Field-stages
from user_stages.field_stages.name import make_name_stage
from user_stages.field_stages.age import make_age_stage
from user_stages.field_stages.sex import make_sex_stage
from user_stages.field_stages.city import make_city_stage
from user_stages.field_stages.photo import make_photo_stage
from user_stages.field_stages.bio import make_bio_stage
from user_stages.field_stages.interests import make_interests_stage

from user_stages.registration import RegistrationStage
from user_stages.match import MatchStage

from user_stages.profile import ProfileStage

from user_stages.freeze import FreezeStage

from user_stages.update_profile import UpdateProfileStage

# Update-extra-stages
from user_stages.update_extra import UpdateExtraStage
from user_stages.field_stages.age import (
    make_min_partner_age_stage, make_max_partner_age_stage)
from user_stages.field_stages.relationship_goal import (
    make_relationship_goal_stage)

from user_stages.info import InfoStage


FIELD_STAGES = [
    make_name_stage("Имя"),
    make_age_stage("Возраст"),
    make_sex_stage("Пол"),
    make_city_stage("Город"),
    make_photo_stage("Фотография"),
    make_bio_stage("Описание"),
    make_interests_stage("Интересы"),
]


# Start-stage
StartStage.next_stage = FIELD_STAGES[0]

# Order forward-stages
for i in range(len(FIELD_STAGES) - 1):
    connect_bydir(FIELD_STAGES[i], FIELD_STAGES[i + 1])
FIELD_STAGES[-1].next_stage = RegistrationStage

# Registration
RegistrationStage.next_stage = ProfileStage

# Profile
ProfileStage.prev_stage = MatchStage

UPDATE_PROFILE_STAGES = [
    make_name_stage("Обновить имя"),
    # make_sex_stage("Обновить пол"), it is forbidden to change sex
    make_age_stage("Обновить возраст"),
    make_city_stage("Обновить город"),
    make_photo_stage("Обновить фото"),
    make_interests_stage("Обновить интересы"),
    make_bio_stage("Обновить описание"),
]

# UpdateProfile
add_alternative_bydir(ProfileStage, UpdateProfileStage)

for stage in UPDATE_PROFILE_STAGES:
    add_alternative_bydir(UpdateProfileStage, stage)
    stage.next_stage = RegistrationStage

# UpdateExtra
add_alternative_bydir(ProfileStage, UpdateExtraStage)
UPDATE_EXTRA_STAGES = [
    make_min_partner_age_stage("Минимальный возраст партнера"),
    make_max_partner_age_stage("Максимальный возраст партнера"),
    make_relationship_goal_stage("Цель отношений"),
]

for stage in UPDATE_EXTRA_STAGES:
    add_alternative_bydir(UpdateExtraStage, stage)
    stage.next_stage = RegistrationStage

# FreezeStage
ProfileStage.add_alternative(FreezeStage)
FreezeStage.next_stage = RegistrationStage


USER_STAGES = (
    [
        StartStage,
        InfoStage,
    ]
    +
    FIELD_STAGES
    +
    [
        RegistrationStage,
        MatchStage,
        ProfileStage,
        FreezeStage,
        UpdateProfileStage,
        UpdateExtraStage,
    ]
    +
    UPDATE_PROFILE_STAGES
    +
    UPDATE_EXTRA_STAGES
)


MENU_STAGES = [StartStage, ProfileStage, InfoStage]
