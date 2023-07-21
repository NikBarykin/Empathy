from stage import Stage
from personal.name import NameStage


Stage.chain_stages(
    [
        NameStage,
        NameStage,
        NameStage,
    ]
)
