from overwrite.base import produce_overwrite_stage
from stage_mapper import personal_mapper

OverwritePersonalStage = produce_overwrite_stage(
    stage_name="о себе",
    mapper=personal_mapper,
)
