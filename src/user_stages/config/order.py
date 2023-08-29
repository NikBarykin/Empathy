"""When this module is imported it connects stages in specific order"""
from stage import forbid_go_back

from .declarations.all_stages import (
    FORWARD_STAGES,
    UPDATE_STAGES,
    StartStage,
    MatchStage,
    RegistrationStage,
    FreezeStage,
)


# Start-stage
forbid_go_back(StartStage)
StartStage.next_stage = FORWARD_STAGES[0]

# Order forward-stages
for i in range(len(FORWARD_STAGES)):
    if i != 0:
        FORWARD_STAGES[i - 1].next_stage = FORWARD_STAGES[i]
FORWARD_STAGES[-1].next_stage = RegistrationStage

# Registration
RegistrationStage.next_stage = MatchStage

# First forward-stage can't go back
forbid_go_back(FORWARD_STAGES[0])

# Freeze-stage
FreezeStage.next_stage = MatchStage

# Order update-stages
for stage in UPDATE_STAGES:
    stage.next_stage = MatchStage
