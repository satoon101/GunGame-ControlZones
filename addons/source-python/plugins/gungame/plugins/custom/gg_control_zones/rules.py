# ../gungame/plugins/custom/gg_control_zones/rules.py

"""Creates the gg_control_zones rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules

# Plugin
from .info import info

# =============================================================================
# >> RULES
# =============================================================================
control_zones_rules = GunGameRules(info.name)
control_zones_rules.register_all_rules()
