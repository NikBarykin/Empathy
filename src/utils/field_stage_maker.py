from typing import Type
from stage import Stage

from field_stage import produce_field_stage


class FieldStageMaker:
    """Sugar"""
    def __init__(self, *field_stage_args, **field_stage_kwargs):
        self.field_stage_args = field_stage_args
        self.field_stage_kwargs = field_stage_kwargs

    def __call__(self, stage_name_arg: str) -> Type[Stage]:
        return produce_field_stage(
            *self.field_stage_args,
            **self.field_stage_kwargs,
            stage_name_arg=stage_name_arg,
        )
