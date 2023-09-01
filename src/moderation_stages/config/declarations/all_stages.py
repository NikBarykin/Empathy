from moderation_stages.moderate import ModerateStage
from moderation_stages.action_choice import ActionChoiceStage
from moderation_stages.statistics import StatisticsStage
from moderation_stages.notify_users import NotifyUsersStage

# every stage that is used in moderation-section
ALL_STAGES = (
    ModerateStage,
    ActionChoiceStage,
    StatisticsStage,
    NotifyUsersStage,
)
