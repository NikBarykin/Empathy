from overwrite.base import produce_overwrite_stage
from stage_mapper import preference_mapper

OverwritePreferenceStage = produce_overwrite_stage(
    stage_name="предподчтения",
    mapper=preference_mapper,
)
