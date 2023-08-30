"""When this module is imported it connects stages in specific order"""
from typing import Type

from stage import Stage

from .declarations.all_stages import (
    FORWARD_STAGES,
    UPDATE_STAGES,
    StartStage,
    MatchStage,
    ChooseUpdateStage,
    ProfileStage,
    RegistrationStage,
    FreezeStage,
)


def connect_bydir(departure: Type[Stage], destination: Type[Stage]):
    """Connect in both directions"""
    departure.next_stage = destination
    destination.prev_stage = departure


# Start-stage
StartStage.next_stage = FORWARD_STAGES[0]

# Order forward-stages
for i in range(len(FORWARD_STAGES) - 1):
    connect_bydir(FORWARD_STAGES[i], FORWARD_STAGES[i + 1])
FORWARD_STAGES[-1].next_stage = RegistrationStage

# Registration
RegistrationStage.next_stage = MatchStage

# Profile-stage
ProfileStage.prev_stage = MatchStage

# Freeze-stage
# We need to notify user's in waiting pool about our unfreeze
FreezeStage.next_stage = RegistrationStage

# update-stages
ChooseUpdateStage.prev_stage = ProfileStage
for stage in UPDATE_STAGES:
    ChooseUpdateStage.add_alternative(stage)
    stage.prev_stage = ChooseUpdateStage
    stage.next_stage = MatchStage
