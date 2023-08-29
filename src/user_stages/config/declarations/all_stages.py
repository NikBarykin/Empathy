from user_stages.start import StartStage
from user_stages.rules import RulesStage
from user_stages.registration import RegistrationStage
from user_stages.match import MatchStage
from user_stages.registration import RegistrationStage
from user_stages.profile import ProfileStage
from user_stages.freeze import FreezeStage
from user_stages.choose_update import ChooseUpdateStage
from .forward_stages import FORWARD_STAGES
from .update_stages import UPDATE_STAGES


ALL_STAGES = (
    [
        StartStage,
        RulesStage,
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
