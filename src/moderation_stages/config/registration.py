from utils.stage_registrar import make_stage_registrar
from .declarations.all_stages import ALL_STAGES


register_moderation_stages = make_stage_registrar(ALL_STAGES)
