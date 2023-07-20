from stage import StageType
from stage import Stage
from typing import Dict, List


StageMapper = Dict[str, StageType]
personal_mapper = {}
preference_mapper = {}


def __init_mapper(stages: List[StageType], mapper: StageMapper) -> None:
    for stage in stages:
        mapper[stage.name] = stage


def init_personal_mapper(personal_stages: List[StageType]) -> None:
    __init_mapper(personal_stages, personal_mapper)


def init_preference_mapper(preference_stages: List[StageType]) -> None:
    __init_mapper(preference_stages, preference_mapper)
