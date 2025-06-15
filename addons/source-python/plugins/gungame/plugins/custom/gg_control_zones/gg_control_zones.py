from events import Event
from filters.players import PlayerIter
from players.teams import teams_by_number

from gungame.core.events.teams import GG_Team_Level_Up, GG_Team_Win
from gungame.core.players.attributes import AttributePreHook
from gungame.core.players.dictionary import player_dictionary
from gungame.core.teams import team_levels
from gungame.core.weapons.manager import weapon_order_manager

from .custom_events import GG_Team_Level_Down

reason_to_method = {
    "lost": "decrease",
    "captured": "increase",
}


@AttributePreHook("level")
def _level_hook(player, attribute, new_value):
    value = team_levels.get(player.team_index)
    if value != new_value:
        return False

    return True


@Event("control_zone_lost")
def _lost_control_zone(game_event):
    team = int(game_event["team"])
    old_level = team_levels[team]
    team_levels[team] -= 1
    set_player_levels(team, reason="lost")
    with GG_Team_Level_Down() as event:
        event.team = team
        event.old_level = old_level
        event.new_value = team_levels[team]
        event.style = "control_zone"


@Event("control_zone_captured")
def _captured_control_zone(game_event):
    team = int(game_event["team"])
    old_level = team_levels[team]
    if old_level == weapon_order_manager.max_levels:
        with GG_Team_Win() as event:
            event.winner = team
            event.loser = 5 - team
            event.style = "control_zones"
        return

    team_levels[team] += 1
    set_player_levels(team, reason="captured")
    with GG_Team_Level_Up() as event:
        event.team = team
        event.old_level = old_level
        event.new_value = team_levels[team]
        event.style = "control_zones"


def set_player_levels(team, reason):
    for player in PlayerIter(teams_by_number[team]):
        getattr(
            player_dictionary[player.userid],
            f"{reason_to_method[reason]}_level",
        )(1, f"control_zone_{reason}")
