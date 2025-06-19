# ../gungame/plugins/custom/gg_control_zones/gg_control_zones.py

"""."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from operator import attrgetter

# Source.Python
from events import Event
from filters.players import PlayerIter
from listeners.tick import Delay
from players.teams import teams_by_number
from plugins.manager import plugin_manager

# Plugin
from gungame.core.events.included.teams import GG_Team_Level_Up, GG_Team_Win
from gungame.core.players.attributes import AttributePreHook
from gungame.core.players.dictionary import player_dictionary
from gungame.core.teams import team_levels
from gungame.core.weapons.manager import weapon_order_manager

from .custom_events import GG_Team_Level_Down

reason_to_method = {
    "lost": "decrease",
    "captured": "increase",
}

if "control_zones" not in map(
    attrgetter("name"),
    plugin_manager.loaded_plugins,
):
    _msg = "Control Zones is not loaded."
    raise ValueError(_msg)


def load():
    _reset_levels()


def unload():
    team_levels.clear()


@AttributePreHook("level")
def _level_hook(player, attribute, new_value):
    value = team_levels.get(player.team_index, 1)
    if value != new_value:
        return False

    return True


@Event("gg_start")
def _reset_levels(game_event=None):
    team_levels.clear(value=1)
    from control_zones.control_zones import control_zones
    if weapon_order_manager.max_levels != len(control_zones):
        msg = "Weapon order length needs to match the number of control zones."
        raise ValueError(msg)


@Event("control_zone_lost")
def _lost_control_zone(game_event):
    team = int(game_event["team"])
    old_level = team_levels[team]
    team_levels[team] -= 1
    _set_player_levels(team, reason="lost")
    with GG_Team_Level_Down() as event:
        event.team = team
        event.old_level = old_level
        event.new_value = team_levels[team]
        event.style = "control_zone"


@Event("control_zone_captured")
def _captured_control_zone(game_event):
    team = int(game_event["team"])
    old_level = team_levels[team]
    team_levels[team] += 1
    _set_player_levels(team, reason="captured")
    if team_levels[team] >= weapon_order_manager.max_levels:
        Delay(0, _fire_team_win, (team,))
        return

    with GG_Team_Level_Up() as event:
        event.team = team
        event.old_level = old_level
        event.new_level = team_levels[team]
        event.style = "control_zones"


def _fire_team_win(team):
    with GG_Team_Win() as event:
        event.winner = team
        event.loser = 5 - team
        event.style = "control_zones"


def _set_player_levels(team, reason):
    for player in PlayerIter(teams_by_number[team]):
        getattr(
            player_dictionary[player.userid],
            f"{reason_to_method[reason]}_level",
        )(1, f"control_zone_{reason}")
