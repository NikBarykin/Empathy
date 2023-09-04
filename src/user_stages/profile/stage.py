"""
Profile stage

When you want to send someone your profile or update/complete you profile
"""
from fork_stage.produce import produce_fork_stage

from .constants import CONTINUE_TEXT, DESCRIPTION
from .logic import get_profile_caption, get_profile_photo


ProfileStage = produce_fork_stage(
    stage_name_arg="my_profile",
    question_text_getter_arg=get_profile_caption,
    prev_stage_button_text_arg=CONTINUE_TEXT,
    question_photo_getter_arg=get_profile_photo,
    description_arg=DESCRIPTION,
)
