# ../gungame/plugins/custom/gg_control_zones/custom_events.py

"""Events used by gg_control_zones."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events.custom import CustomEvent
from events.variable import ByteVariable, ShortVariable, StringVariable

# GunGame
from gungame.core.events.resource import GGResourceFile

# Plugin
from .info import info

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "GG_Team_Level_Down",
)


# =============================================================================
# >> CLASSES
# =============================================================================
# ruff: noqa: N801
class GG_Team_Level_Down(CustomEvent):
    """Called during team-based play when a team levels down."""

    team = ShortVariable("The team that leveled up")
    old_level = ByteVariable("The old level of the team that leveled down")
    new_level = ByteVariable("The new level of the team that leveled down")
    style = StringVariable("The style of teamplay match")


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGResourceFile(info.name, GG_Team_Level_Down)
