from stages.regular_workflow.start import StartStage
from stages.regular_workflow.registration import RegistrationStage
from stages.regular_workflow.match import MatchStage
from stages.regular_workflow.registration import RegistrationStage
from stages.regular_workflow.profile import ProfileStage
from stages.regular_workflow.freeze import FreezeStage
from stages.regular_workflow.choose_update import ChooseUpdateStage
from .forward_stages import FORWARD_STAGES
from .update_stages import UPDATE_STAGES


ALL_STAGES = (
    [
        StartStage
    ]
    +
    FORWARD_STAGES
    +
    [
        RegistrationStage,
        MatchStage,
        RegistrationStage,
        ProfileStage,
        FreezeStage,
        ChooseUpdateStage,
    ]
    +
    UPDATE_STAGES
)
