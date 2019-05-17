from basketball_reference_web_scraper.utilities import str_to_str, str_to_float, str_to_int
from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM, POSITION_ABBREVIATIONS_TO_POSITION


def extract_name_rows_from_table(tab, required_classes, excluded_row_classes):
    if not tab.has_attr('class'):
        return None, None

    if False in [k in tab['class'] for k in required_classes]:
        return None, None

    else:
        name = tab.find('caption').text.strip()
        name = name.upper()

        ## get all rows that we don't exclude due to their class, that have a table cell, and 
        ## where that first table cell is not 'Team Totals' (cause I don't want those rows)
        rows = [row.find_all('td') for row in tab.find_all('tr') if (
            row.find('th') is not None and
            True not in [exclud_class in row.find('th')['class'] for exclud_class in excluded_row_classes] and
            row.find('td') is not None and
            row.find('td').text != 'Team Totals')]

        return name, rows

def get_all_tables_with_soup(page, required_classes=['stats_table', 'sortable'], 
        excluded_row_classes=['over_header', 'poptip']):
    from bs4 import BeautifulSoup, Comment
    soup = BeautifulSoup(page, 'lxml')
    all_tables = {}

    ## first handle all the commented out tables
    for comment in soup.find_all(string=lambda text:  isinstance(text, Comment)):
        data = BeautifulSoup(comment, 'lxml')
        tables = data.find_all('table')
        for tab in tables:
            name, rows = extract_name_rows_from_table(tab, required_classes, excluded_row_classes)
            if name is not None:
                all_tables[name] = rows

    ## now handle the uncommented tables:
    for tab in soup.find_all('table'):
        name, rows = extract_name_rows_from_table(tab, required_classes, excluded_row_classes)
        if name is not None:
            all_tables[name] = rows
    return all_tables

def parse_team(value):
    return TEAM_ABBREVIATIONS_TO_TEAM[value]

def parse_team_as_string(value):
    return TEAM_ABBREVIATIONS_TO_TEAM[value].value

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

def extract_player_name(name_id_content):
    return name_id_content.split('\\')[0].replace('*', '')

def extract_player_id(name_id_content):
    return name_id_content.split('\\')[1]

def parse_max_minutes_played(time_content):
    if not len(time_content):
        return 0
    elif ':' not in time_content:
        return str_to_float(time_content)
    else:
        minutes, seconds = time_content.split(':')
        return str_to_float(minutes) + str_to_float(seconds)/60

def parse_percent_time(percent_time_content):
    if not len(percent_time_content):
        return 0.0
    return float(percent_time_content.strip('%'))

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
    "OBPM"                 : "offensive_box_plus_minus",
    "DBPM"                 : "defensive_box_plus_minus",
    "BPM"                  : "total_box_plus_minus",
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
    'Player'               : 'player',
    ### per game numbers:
    'MPpg'                 : 'minutes_played_per_game',
    'PTSpg'                : 'points_per_game',
    'TRBpg'                : 'total_rebounds_per_game',
    'ASTpg'                : 'assists_per_game',
    'STLpg'                : 'steals_per_game',
    'BLKpg'                : 'blocks_per_game',
    'MP_max'               : 'most_minutes_played',
    'ORtg'                 : 'offensive_rating',
    'DRtg'                 : 'defensive_rating',
    'FGpg'                 : 'made_field_goals_per_game',
    'FGApg'                : 'attempted_field_goals_per_game',
    '3Ppg'                 : 'made_three_point_field_goals',
    '3PApg'                : 'attempted_three_point_field_goals_per_game',
    '2Ppg'                 : 'made_two_point_field_goals_per_game',
    '2PApg'                : 'attempted_two_point_field_goals_per_game',
    'FTpg'                 : 'made_free_throws_per_game',
    'FTApg'                : 'attempted_free_throws_per_game',
    'ORBpg'                : 'offensive_rebounds_per_game',
    'DRBpg'                : 'defensive_rebounds_per_game',
    'TRBpg'                : 'total_rebounds_per_game',
    'ASTpg'                : 'assists_per_game',
    'STLpg'                : 'steals_per_game',
    'BLKpg'                : 'blocks_per_game',
    'TOVpg'                : 'turnovers_per_game',
    'PFpg'                 : 'personal_fouls_per_game',
    'PTSpg'                : 'points_per_game',
    ### per 36 minutes numbers:
    'MPper36'                 : 'minutes_played_per_36_minutes',
    'PTSper36'                : 'points_per_36_minutes',
    'TRBper36'                : 'total_rebounds_per_36_minutes',
    'ASTper36'                : 'assists_per_36_minutes',
    'STLper36'                : 'steals_per_36_minutes',
    'BLKper36'                : 'blocks_per_36_minutes',
    'MP_mper36'               : 'most_minutes_pl36_minutes',
    'ORper36'                 : 'offensive_ra36_minutes',
    'DRper36'                 : 'defensive_ra36_minutes',
    'FGper36'                 : 'made_field_goals_per_36_minutes',
    'FGAper36'                : 'attempted_field_goals_per_36_minutes',
    '3Pper36'                 : 'made_three_point_field_g36_minutes',
    '3PAper36'                : 'attempted_three_point_field_goals_per_36_minutes',
    '2Pper36'                 : 'made_two_point_field_goals_per_36_minutes',
    '2PAper36'                : 'attempted_two_point_field_goals_per_36_minutes',
    'FTper36'                 : 'made_free_throws_per_36_minutes',
    'FTAper36'                : 'attempted_free_throws_per_36_minutes',
    'ORBper36'                : 'offensive_rebounds_per_36_minutes',
    'DRBper36'                : 'defensive_rebounds_per_36_minutes',
    'TRBper36'                : 'total_rebounds_per_36_minutes',
    'ASTper36'                : 'assists_per_36_minutes',
    'STLper36'                : 'steals_per_36_minutes',
    'BLKper36'                : 'blocks_per_36_minutes',
    'TOVper36'                : 'turnovers_per_36_minutes',
    'PFper36'                 : 'personal_fouls_per_36_minutes',
    'PTSper36'                : 'points_per_36_minutes',
    ### per 100 possessions numbers:
    'MPperposs'                 : 'minutes_played_per_100_poss',
    'PTSperposs'                : 'points_per_100_poss',
    'TRBperposs'                : 'total_rebounds_per_100_poss',
    'ASTperposs'                : 'assists_per_100_poss',
    'STLperposs'                : 'steals_per_100_poss',
    'BLKperposs'                : 'blocks_per_100_poss',
    'MP_mperposs'               : 'most_minutes_pl100_poss',
    'ORperposs'                 : 'offensive_ra100_poss',
    'DRperposs'                 : 'defensive_ra100_poss',
    'FGperposs'                 : 'made_field_goals_per_100_poss',
    'FGAperposs'                : 'attempted_field_goals_per_100_poss',
    '3Pperposs'                 : 'made_three_point_field_g100_poss',
    '3PAperposs'                : 'attempted_three_point_field_goals_per_100_poss',
    '2Pperposs'                 : 'made_two_point_field_goals_per_100_poss',
    '2PAperposs'                : 'attempted_two_point_field_goals_per_100_poss',
    'FTperposs'                 : 'made_free_throws_per_100_poss',
    'FTAperposs'                : 'attempted_free_throws_per_100_poss',
    'ORBperposs'                : 'offensive_rebounds_per_100_poss',
    'DRBperposs'                : 'defensive_rebounds_per_100_poss',
    'TRBperposs'                : 'total_rebounds_per_100_poss',
    'ASTperposs'                : 'assists_per_100_poss',
    'STLperposs'                : 'steals_per_100_poss',
    'BLKperposs'                : 'blocks_per_100_poss',
    'TOVperposs'                : 'turnovers_per_100_poss',
    'PFperposs'                 : 'personal_fouls_per_100_poss',
    'PTSperposs'                : 'points_per_100_poss',
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
    "3P"                   : str_to_int,
    "3PA"                  : str_to_int,
    "2P"                   : str_to_int,
    "2PA"                  : str_to_int,
    "FT"                   : str_to_int,
    "FTA"                  : str_to_int,
    "ORB"                  : str_to_int,
    "DRB"                  : str_to_int,
    "TRB"                  : str_to_int,
    "AST"                  : str_to_int,
    "STL"                  : str_to_int,
    "BLK"                  : str_to_int,
    "TOV"                  : str_to_int,
    "PF"                   : str_to_int,
    "PTS"                  : str_to_int,
    "dunk_Md."             : str_to_int,
    "heave_Att."           : str_to_int,
    "heave_Md."            : str_to_int,
    'TOV_BadPass'          : str_to_int,
    'TOV_LostBall'         : str_to_int,
    'Shooting_fouls_cmt'   : str_to_int,
    'Offensive_fouls_cmt'  : str_to_int,
    'Shooting_fouls_drwn'  : str_to_int,
    'Offensive_fouls_drwn' : str_to_int,
    'PGA'                  : str_to_int,
    'And1'                 : str_to_int,
    'Blkd'                 : str_to_int,
    'MP_max'               : parse_max_minutes_played,
    'PG%'                  : parse_percent_time,
    'SG%'                  : parse_percent_time,
    'SF%'                  : parse_percent_time,
    'PF%'                  : parse_percent_time,
    'C%'                   : parse_percent_time,
}

for k in COLUMN_RENAMER:
    if k not in COLUMN_PARSER:
        COLUMN_PARSER[k] = str_to_float

def parse_souped_row_given_header_columns(row, header_columns):
    """
    parse a single row (from a tr.find_all('td')) given a list of column names

    leverages COLUMN_RENAMER and COLUMN_PARSER to get output names
    and the datatype of each column, though in principle can just pull
    from the data included in the td....  might switch to that 
    eventually, but I worry about mixing up/overlaps, which I've
    already taken care of by hand. 
    """
    assert len(header_columns) == len(row), "mismatch between row length and header length"

    to_return = {}
    for ii, key in enumerate(header_columns):
        if header_columns[ii] == 'empty':
            continue
        elif header_columns[ii] == 'Player':
            ## split player into player_name and player_id
            to_return['player_id'] = row[ii].get('data-append-csv')
            ## drop the star for a player's name that indicates they're in the hall of fame
            to_return['player_name'] = row[ii].text.replace('*', '')
        else:
            # print(key, COLUMN_RENAMER[key], COLUMN_PARSER[key], row[ii].text)
            to_return[COLUMN_RENAMER[key]] = COLUMN_PARSER[key](row[ii].text)
    return to_return

def find_team_column(header_columns):
    return header_columns.index('Tm')

def split_header_columns(header_string):
    return header_string.split(",")