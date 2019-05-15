from enum import Enum

from basketball_reference_web_scraper.utilities import str_to_str, str_to_float, str_to_int


class Location(Enum):
    HOME = "HOME"
    AWAY = "AWAY"


class Outcome(Enum):
    WIN = "WIN"
    LOSS = "LOSS"


class Team(Enum):
    ATLANTA_HAWKS = "ATLANTA HAWKS"
    BOSTON_CELTICS = "BOSTON CELTICS"
    BROOKLYN_NETS = "BROOKLYN NETS"
    CHARLOTTE_HORNETS = "CHARLOTTE HORNETS"
    CHICAGO_BULLS = "CHICAGO BULLS"
    CLEVELAND_CAVALIERS = "CLEVELAND CAVALIERS"
    DALLAS_MAVERICKS = "DALLAS MAVERICKS"
    DENVER_NUGGETS = "DENVER NUGGETS"
    DETROIT_PISTONS = "DETROIT PISTONS"
    GOLDEN_STATE_WARRIORS = "GOLDEN STATE WARRIORS"
    HOUSTON_ROCKETS = "HOUSTON ROCKETS"
    INDIANA_PACERS = "INDIANA PACERS"
    LOS_ANGELES_CLIPPERS = "LOS ANGELES CLIPPERS"
    LOS_ANGELES_LAKERS = "LOS ANGELES LAKERS"
    MEMPHIS_GRIZZLIES = "MEMPHIS GRIZZLIES"
    MIAMI_HEAT = "MIAMI HEAT"
    MILWAUKEE_BUCKS = "MILWAUKEE BUCKS"
    MINNESOTA_TIMBERWOLVES = "MINNESOTA TIMBERWOLVES"
    NEW_ORLEANS_PELICANS = "NEW ORLEANS PELICANS"
    NEW_YORK_KNICKS = "NEW YORK KNICKS"
    OKLAHOMA_CITY_THUNDER = "OKLAHOMA CITY THUNDER"
    ORLANDO_MAGIC = "ORLANDO MAGIC"
    PHILADELPHIA_76ERS = "PHILADELPHIA 76ERS"
    PHOENIX_SUNS = "PHOENIX SUNS"
    PORTLAND_TRAIL_BLAZERS = "PORTLAND TRAIL BLAZERS"
    SACRAMENTO_KINGS = "SACRAMENTO KINGS"
    SAN_ANTONIO_SPURS = "SAN ANTONIO SPURS"
    TORONTO_RAPTORS = "TORONTO RAPTORS"
    UTAH_JAZZ = "UTAH JAZZ"
    WASHINGTON_WIZARDS = "WASHINGTON WIZARDS"

    # DEPRECATED TEAMS
    CHARLOTTE_BOBCATS = "CHARLOTTE BOBCATS"
    NEW_JERSEY_NETS = "NEW JERSEY NETS"
    NEW_ORLEANS_HORNETS = "NEW ORLEANS HORNETS"
    NEW_ORLEANS_OKLAHOMA_CITY_HORNETS = "NEW ORLEANS/OKLAHOMA CITY HORNETS"
    SEATTLE_SUPERSONICS = "SEATTLE SUPERSONICS"
    VANCOUVER_GRIZZLIES = "VANCOUVER GRIZZLIES"


class OutputType(Enum):
    JSON = "JSON"
    CSV = "CSV"


class OutputWriteOption(Enum):
    WRITE = "w"
    CREATE_AND_WRITE = "w+"
    APPEND = "a"
    APPEND_AND_WRITE = "a+"


class Position(Enum):
    POINT_GUARD = "POINT GUARD"
    SHOOTING_GUARD = "SHOOTING GUARD"
    SMALL_FORWARD = "SMALL FORWARD"
    POWER_FORWARD = "POWER FORWARD"
    CENTER = "CENTER"
    FORWARD = "FORWARD"
    GUARD = "GUARD"


TEAM_ABBREVIATIONS_TO_TEAM = {
    'ATL': Team.ATLANTA_HAWKS,
    'BOS': Team.BOSTON_CELTICS,
    'BRK': Team.BROOKLYN_NETS,
    'CHI': Team.CHICAGO_BULLS,
    'CHO': Team.CHARLOTTE_HORNETS,
    'CLE': Team.CLEVELAND_CAVALIERS,
    'DAL': Team.DALLAS_MAVERICKS,
    'DEN': Team.DENVER_NUGGETS,
    'DET': Team.DETROIT_PISTONS,
    'GSW': Team.GOLDEN_STATE_WARRIORS,
    'HOU': Team.HOUSTON_ROCKETS,
    'IND': Team.INDIANA_PACERS,
    'LAC': Team.LOS_ANGELES_CLIPPERS,
    'LAL': Team.LOS_ANGELES_LAKERS,
    'MEM': Team.MEMPHIS_GRIZZLIES,
    'MIA': Team.MIAMI_HEAT,
    'MIL': Team.MILWAUKEE_BUCKS,
    'MIN': Team.MINNESOTA_TIMBERWOLVES,
    'NOP': Team.NEW_ORLEANS_PELICANS,
    'NYK': Team.NEW_YORK_KNICKS,
    'OKC': Team.OKLAHOMA_CITY_THUNDER,
    'ORL': Team.ORLANDO_MAGIC,
    'PHI': Team.PHILADELPHIA_76ERS,
    'PHO': Team.PHOENIX_SUNS,
    'POR': Team.PORTLAND_TRAIL_BLAZERS,
    'SAC': Team.SACRAMENTO_KINGS,
    'SAS': Team.SAN_ANTONIO_SPURS,
    'TOR': Team.TORONTO_RAPTORS,
    'UTA': Team.UTAH_JAZZ,
    'WAS': Team.WASHINGTON_WIZARDS,

    # DEPRECATED TEAMS
    'NJN': Team.NEW_JERSEY_NETS,
    'NOH': Team.NEW_ORLEANS_HORNETS,
    'NOK': Team.NEW_ORLEANS_OKLAHOMA_CITY_HORNETS,
    'CHA': Team.CHARLOTTE_BOBCATS,
    'CHH': Team.CHARLOTTE_HORNETS,
    'SEA': Team.SEATTLE_SUPERSONICS,
    'VAN': Team.VANCOUVER_GRIZZLIES,
}

TEAM_NAME_TO_TEAM = {
    "ATLANTA HAWKS": Team.ATLANTA_HAWKS,
    "BOSTON CELTICS": Team.BOSTON_CELTICS,
    "BROOKLYN NETS": Team.BROOKLYN_NETS,
    "CHARLOTTE HORNETS": Team.CHARLOTTE_HORNETS,
    "CHICAGO BULLS": Team.CHICAGO_BULLS,
    "CLEVELAND CAVALIERS": Team.CLEVELAND_CAVALIERS,
    "DALLAS MAVERICKS": Team.DALLAS_MAVERICKS,
    "DENVER NUGGETS": Team.DENVER_NUGGETS,
    "DETROIT PISTONS": Team.DETROIT_PISTONS,
    "GOLDEN STATE WARRIORS": Team.GOLDEN_STATE_WARRIORS,
    "HOUSTON ROCKETS": Team.HOUSTON_ROCKETS,
    "INDIANA PACERS": Team.INDIANA_PACERS,
    "LOS ANGELES CLIPPERS": Team.LOS_ANGELES_CLIPPERS,
    "LOS ANGELES LAKERS": Team.LOS_ANGELES_LAKERS,
    "MEMPHIS GRIZZLIES": Team.MEMPHIS_GRIZZLIES,
    "MIAMI HEAT": Team.MIAMI_HEAT,
    "MILWAUKEE BUCKS": Team.MILWAUKEE_BUCKS,
    "MINNESOTA TIMBERWOLVES": Team.MINNESOTA_TIMBERWOLVES,
    "NEW ORLEANS PELICANS": Team.NEW_ORLEANS_PELICANS,
    "NEW YORK KNICKS": Team.NEW_YORK_KNICKS,
    "OKLAHOMA CITY THUNDER": Team.OKLAHOMA_CITY_THUNDER,
    "ORLANDO MAGIC": Team.ORLANDO_MAGIC,
    "PHILADELPHIA 76ERS": Team.PHILADELPHIA_76ERS,
    "PHOENIX SUNS": Team.PHOENIX_SUNS,
    "PORTLAND TRAIL BLAZERS": Team.PORTLAND_TRAIL_BLAZERS,
    "SACRAMENTO KINGS": Team.SACRAMENTO_KINGS,
    "SAN ANTONIO SPURS": Team.SAN_ANTONIO_SPURS,
    "TORONTO RAPTORS": Team.TORONTO_RAPTORS,
    "UTAH JAZZ": Team.UTAH_JAZZ,
    "WASHINGTON WIZARDS": Team.WASHINGTON_WIZARDS,

    # DEPRECATED TEAMS
    "CHARLOTTE BOBCATS": Team.CHARLOTTE_BOBCATS,
    "NEW JERSEY NETS": Team.NEW_JERSEY_NETS,
    "NEW ORLEANS HORNETS": Team.NEW_ORLEANS_HORNETS,
    "NEW ORLEANS/OKLAHOMA CITY HORNETS": Team.NEW_ORLEANS_OKLAHOMA_CITY_HORNETS,
    "SEATTLE SUPERSONICS": Team.SEATTLE_SUPERSONICS,
    "VANCOUVER GRIZZLIES": Team.VANCOUVER_GRIZZLIES,
}

POSITION_ABBREVIATIONS_TO_POSITION = {
    "PG": Position.POINT_GUARD,
    "SG": Position.SHOOTING_GUARD,
    "SF": Position.SMALL_FORWARD,
    "PF": Position.POWER_FORWARD,
    "C": Position.CENTER,
    "F": Position.FORWARD,
    "G": Position.GUARD,
}

def parse_team(value):
    return TEAM_ABBREVIATIONS_TO_TEAM.get(value)

def parse_team_as_string(value):
    return TEAM_ABBREVIATIONS_TO_TEAM.get(value).value

def parse_positions(positions_content):
    parsed_positions = list(
        map(
            lambda position_abbreviation: POSITION_ABBREVIATIONS_TO_POSITION.get(position_abbreviation),
            positions_content.split("-")
        )
    )
    return [position for position in parsed_positions if position is not None]

def parse_positions_as_string(positions_content):
    return '-'.join([position.value for position in parse_positions(positions_content)])

COLUMN_RENAMER = {
    "empty"                : "empty",
    "Season"               : "season",
    "Age"                  : "age",
    "Tm"                   : "team",
    "Lg"                   : "league",
    "Pos"                  : "positions",
    "G"                    : "games_played",
    "GS"                   : "games_started",
    "MP"                   : "minutes_played",
    "FG"                   : "made_field_goals",
    "FGA"                  : "attempted_field_goals",
    "FG%"                  : "free_throw_percent",
    "3P"                   : "made_three_point_field_goals",
    "3PA"                  : "attempted_three_point_field_goals",
    "3P%"                  : "three_point_percent",
    "2P"                   : "made_two_point_field_goals",
    "2PA"                  : "attempted_two_point_field_goals",
    "2P%"                  : "two_point_percent",
    "eFG%"                 : "effective_field_goal_percent",
    "FT"                   : "made_free_throws",
    "FTA"                  : "attempted_free_throws",
    "FT%"                  : "free_throw_percent",
    "ORB"                  : "offensive_rebounds",
    "DRB"                  : "defensive_rebounds",
    "TRB"                  : "total_rebounds",
    "AST"                  : "assists",
    "STL"                  : "steals",
    "BLK"                  : "blocks",
    "TOV"                  : "turnovers",
    "PF"                   : "personal_fouls",
    "PTS"                  : "points",
    "PER"                  : "player_efficiency_rating",
    "TS%"                  : "true_shooting_percent",
    "3PAr"                 : "three_point_attempt_rate",
    "FTr"                  : "free_throw_attempt_rate",
    "ORB%"                 : "offensive_rebound_pct",
    "DRB%"                 : "defensive_rebound_pct",
    "TRB%"                 : "total_rebound_pct",
    "AST%"                 : "assists_pct",
    "STL%"                 : "steals_pct",
    "BLK%"                 : "blocks_pct",
    "TOV%"                 : "turnover_pct",
    "USG%"                 : "usage_pct",
    "OWS"                  : "offensive_win_shares",
    "DWS"                  : "defensive_win_shares",
    "WS"                   : "total_win_shares",
    "WS/48"                : "total_win_shares_per_48",
    "OBPM"                 : "offensive_bpm",
    "DBPM"                 : "defensive_bpm",
    "BPM"                  : "total_bpm",
    "VORP"                 : "vorp",
    "Dist."                : "average_shot_distance",
    "a2P%"                 : "percent_two_point_field_goal_attempts",
    "a0-3"                 : "percent_field_goal_attempts_0-3ft",
    "a3-10"                : "percent_field_goal_attempts_3-10ft",
    "a10-16"               : "percent_field_goal_attempts_10-16ft",
    "a16-3pt"              : "percent_field_goal_attempts_16ft-3pt",
    "a3P%"                 : "percent_three_point_field_goal_attempts",
    "m2P%"                 : "percent_two_point_field_goal_makes",
    "m0-3"                 : "percent_field_goal_makes_0-3ft",
    "m3-10"                : "percent_field_goal_makes_3-10ft",
    "m10-16"               : "percent_field_goal_makes_10-16ft",
    "m16-3pt"              : "percent_field_goal_makes_16ft-3pt",
    "m3P%"                 : "percent_three_point_field_goal_makes",
    "2pt_%Astd"            : "percent_two_point_field_goals_assisted",
    "dunk_%FGA"            : "percent_of_two_pointers_that_are_dunks",
    "dunk_Md."             : "number_of_dunks",
    "3pt_%Astd"            : "percent_three_point_field_goals_assisted",
    "corner_%3PA"          : "percent_three_point_field_goals_attempted_from_corner",
    "corner_3P%"           : "percent_three_point_field_goals_made_from_corner",
    "heave_Att."           : "attempted_heaves",
    "heave_Md."            : "made_heaves",
    'PG%'                  : "percent_time_at_point_guard",
    'SG%'                  : "percent_time_at_shooting_guard",
    'SF%'                  : "percent_time_at_small_forward",
    'PF%'                  : "percent_time_at_power_forward",
    'C%'                   : "percent_time_at_center",
    '+/per100_OnCourt'     : "plus_minus_per_100_possessions",
    '+/-_per100_On-Off'    : "net_plus_minus_per_100_possessions",
    'TOV_BadPass'          : "bad_pass_turnovers",
    'TOV_LostBall'         : "lost_ball_turnovers",
    'Shooting_fouls_cmt'   : "shooting_fouls_committed",
    'Offensive_fouls_cmt'  : "offensive_fouls_committed",
    'Shooting_fouls_drwn'  : "shooting_fouls_drawn",
    'Offensive_fouls_drwn' : "offensive_fouls_drawn",
    'PGA'                  : "points_generated_by_assists",
    'And1'                 : "and_ones",
    'Blkd'                 : "blocked_field_goal_attempts",
    'GmSc'                 : 'game_score',
}


COLUMN_PARSER = {
    "Season"               : str_to_str,
    "Age"                  : str_to_int,
    "Tm"                   : parse_team_as_string,
    "Lg"                   : str_to_str,
    "Pos"                  : parse_positions_as_string,
    "G"                    : str_to_int,
    "GS"                   : str_to_int,
    "MP"                   : str_to_int,
    "FG"                   : str_to_int,
    "FGA"                  : str_to_int,
    "FG%"                  : str_to_float,
    "3P"                   : str_to_int,
    "3PA"                  : str_to_int,
    "3P%"                  : str_to_float,
    "2P"                   : str_to_int,
    "2PA"                  : str_to_int,
    "2P%"                  : str_to_float,
    "eFG%"                 : str_to_float,
    "FT"                   : str_to_int,
    "FTA"                  : str_to_int,
    "FT%"                  : str_to_float,
    "ORB"                  : str_to_int,
    "DRB"                  : str_to_int,
    "TRB"                  : str_to_int,
    "AST"                  : str_to_int,
    "STL"                  : str_to_int,
    "BLK"                  : str_to_int,
    "TOV"                  : str_to_int,
    "PF"                   : str_to_int,
    "PTS"                  : str_to_int,
    "PER"                  : str_to_float,
    "TS%"                  : str_to_float,
    "3PAr"                 : str_to_float,
    "FTr"                  : str_to_float,
    "ORB%"                 : str_to_float,
    "DRB%"                 : str_to_float,
    "TRB%"                 : str_to_float,
    "AST%"                 : str_to_float,
    "STL%"                 : str_to_float,
    "BLK%"                 : str_to_float,
    "TOV%"                 : str_to_float,
    "USG%"                 : str_to_float,
    "OWS"                  : str_to_float,
    "DWS"                  : str_to_float,
    "WS"                   : str_to_float,
    "WS/48"                : str_to_float,
    "OBPM"                 : str_to_float,
    "DBPM"                 : str_to_float,
    "BPM"                  : str_to_float,
    "VORP"                 : str_to_float,
    "Dist."                : str_to_float,
    "a2P%"                 : str_to_float,
    "a0-3"                 : str_to_float,
    "a3-10"                : str_to_float,
    "a10-16"               : str_to_float,
    "a16-3pt"              : str_to_float,
    "a3P%"                 : str_to_float,
    "m2P%"                 : str_to_float,
    "m0-3"                 : str_to_float,
    "m3-10"                : str_to_float,
    "m10-16"               : str_to_float,
    "m16-3pt"              : str_to_float,
    "m3P%"                 : str_to_float,
    "2pt_%Astd"            : str_to_float,
    "dunk_%FGA"            : str_to_float,
    "dunk_Md."             : str_to_int,
    "3pt_%Astd"            : str_to_float,
    "corner_%3PA"          : str_to_float,
    "corner_3P%"           : str_to_float,
    "heave_Att."           : str_to_int,
    "heave_Md."            : str_to_int,
    'PG%'                  : str_to_float,
    'SG%'                  : str_to_float,
    'SF%'                  : str_to_float,
    'PF%'                  : str_to_float,
    'C%'                   : str_to_float,
    '+/per100_OnCourt'     : str_to_float,
    '+/-_per100_On-Off'    : str_to_float,
    'TOV_BadPass'          : str_to_int,
    'TOV_LostBall'         : str_to_int,
    'Shooting_fouls_cmt'   : str_to_int,
    'Offensive_fouls_cmt'  : str_to_int,
    'Shooting_fouls_drwn'  : str_to_int,
    'Offensive_fouls_drwn' : str_to_int,
    'PGA'                  : str_to_int,
    'And1'                 : str_to_int,
    'Blkd'                 : str_to_int,
    'GmSc'                 : str_to_float,
}
