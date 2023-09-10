from utils.order import add_alternative_bydir

from moderation_stages.moderate import ModerateStage
from moderation_stages.action_choice import ActionChoiceStage
from moderation_stages.statistics import StatisticsStage
from moderation_stages.notify_users import NotifyUsersStage


ModerateStage.next_stage = ActionChoiceStage

# Stats
ActionChoiceStage.add_alternative(StatisticsStage)
StatisticsStage.next_stage = ActionChoiceStage

# Notify users
add_alternative_bydir(ActionChoiceStage, NotifyUsersStage)
NotifyUsersStage.next_stage = ActionChoiceStage

MODERATION_STAGES = [
    ModerateStage,
    ActionChoiceStage,
    StatisticsStage,
    NotifyUsersStage,
]
