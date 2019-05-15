from lxml import html

from basketball_reference_web_scraper.utilities import merge_two_dicts
from basketball_reference_web_scraper.data  import TEAM_ABBREVIATIONS_TO_TEAM, COLUMN_RENAMER, COLUMN_PARSER
from basketball_reference_web_scraper.parsers.common import find_team_column, \
    parse_row_given_header_column, split_header_columns


### set list of aliases allowed for the different tables
__per_game_names = ['per_game', 'per game', 'per-game', 'pergame']
__totals_names = ['totals', 'total']
__per_minute_names = ['per_minute', 'per_36_minutes', 'per_36', 'per36', 
                'per 36', 'per 36 minutes', 'per-36', 'per-36-minutes']
__per_poss_names = ['per_poss', 'per_100_possessions', 'per_100', 'per100', 
        'per 100 posessions', 'per 100', 'per-100-possessions', 
        'per100poss', 'per_100_poss', 'per 100 poss', 'per-100-poss',]
__advanced_names = ['advanced']
__shooting_names = ['shooting']
__pbp_names = ['pbp', 'play-by-play', 'play_by_play', 'play by play']
__game_high_names = ['year-and-career-highs', 'game highs', 'game-highs', 'game_highs']

__base_career_tables = (__per_game_names + __totals_names + 
        __per_minute_names + __per_poss_names + __advanced_names + 
        __shooting_names + __pbp_names)

__playoff_career_tables = ['playoffs_'+k for k in __base_career_tables]

__build_key_rename_keys_list = lambda outkey, list:  [(item, outkey) for item in list]
__base_career_table_renamer = dict(
    __build_key_rename_keys_list('per_game', __per_game_names) + 
    __build_key_rename_keys_list('totals', __totals_names) + 
    __build_key_rename_keys_list('per_minute', __per_minute_names) + 
    __build_key_rename_keys_list('per_poss', __per_poss_names) + 
    __build_key_rename_keys_list('advanced', __advanced_names) + 
    __build_key_rename_keys_list('shooting', __shooting_names) + 
    __build_key_rename_keys_list('pbp', __pbp_names) +
    __build_key_rename_keys_list('year-and-career-highs', __game_high_names))

### note -- there is no year-and-career-highs table for the playoffs
__playoff_career_table_renamer = dict([('playoffs_'+k, 'playoffs_'+v) 
    for (k, v) in __base_career_table_renamer.items() if v != 'year-and-career-highs'])

career_table_renamer = merge_two_dicts(
    __base_career_table_renamer, __playoff_career_table_renamer)

## per-game, totals, per 36 minutes, and per 100 posessions all use this:
__career_base_header = "Season,Age,Tm,Lg,Pos,G,GS,MP,FG,FGA,FG%,3P,3PA,3P%,2P,2PA,2P%,eFG%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS"
__career_base_header_columns = split_header_columns(__career_base_header)

__career_advanced_header = "Season,Age,Tm,Lg,Pos,G,MP,PER,TS%,3PAr,FTr,ORB%,DRB%,TRB%,AST%,STL%,BLK%,TOV%,USG%,empty,OWS,DWS,WS,WS/48,empty,OBPM,DBPM,BPM,VORP"
__career_advanced_header_columns = split_header_columns(__career_advanced_header)

__career_shooting_header = "Season,Age,Tm,Lg,Pos,G,MP,FG%,Dist.,a2P%,a0-3,a3-10,a10-16,a16-3pt,a3P%,m2P%,m0-3,m3-10,m10-16,m16-3pt,m3P%,2pt_%Astd,dunk_%FGA,dunk_Md.,3pt_%Astd,corner_%3PA,corner_3P%,heave_Att.,heave_Md."
__career_shooting_header_columns = split_header_columns(__career_shooting_header)

__career_play_by_play_header = "Season,Age,Tm,Lg,Pos,G,MP,PG%,SG%,SF%,PF%,C%,+/per100_OnCourt,+/-_per100_On-Off,TOV_BadPass,TOV_LostBall,Shooting_fouls_cmt,Offensive_fouls_cmt,Shooting_fouls_drwn,Offensive_fouls_drwn,PGA,And1,Blkd"
__career_play_by_play_header_columns = split_header_columns(__career_play_by_play_header)

__career_game_highs_header = "Season,Age,Tm,Lg,MP,FG,FGA,3P,3PA,2P,2PA,FT,FTA,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,GmSc"
__career_game_highs_header_columns = split_header_columns(__career_game_highs_header)

__base_career_table_headers = {
    'per_game'              : __career_base_header_columns,
    'totals'                : __career_base_header_columns,
    'per_minute'            : __career_base_header_columns,
    'per_poss'              : __career_base_header_columns,
    'advanced'              : __career_advanced_header_columns,
    'shooting'              : __career_shooting_header_columns,
    'pbp'                   : __career_play_by_play_header_columns,
    'year-and-career-highs' : __career_game_highs_header_columns,
}

## note that playoff tables have identical headers as regular season tables
## so use the same header columns for the playoff tables as the regular columns
## but remember that there's again no playoffs version of year-and-career-highs
__playoff_career_table_headers = dict([('playoffs_'+k, v) 
    for (k, v) in __base_career_table_headers.items() if k != 'year-and-career-highs'])

career_table_headers = merge_two_dicts(
    __base_career_table_headers, __playoff_career_table_headers)

VALID_CAREER_TABLE_NAMES = __base_career_tables + __playoff_career_tables
UNIQUE_CAREER_TABLES = list(set(career_table_renamer.values()))

def get_table_rows(tree, div_id):
    divs = tree.xpath('//div[@id="{div_id}"]'.format(div_id=div_id))
    if len(divs) != 1:
        raise IOError("Got incorrect number of divs for {div_id} (expected 1, got {num_divs})".format(
            div_id=div_id, num_divs=len(divs)))

    div = divs[0]

    ## grab all table rows within this div, since I've already trimmed the page down to the div I want
    rows = div.xpath('//table/tbody/tr')
    return rows

def get_divid_headercolumns(table):
    """
    get the id string to search for in the page and the headers for a table
    """
    if table not in career_table_renamer:
        msg = "Don't know how to get table {table}.  Must be one of: ".format(table=table)
        msg += ', '.join(list(career_table_renamer.keys()))
        raise KeyError(msg)

    resolved_table = career_table_renamer[table]
    
    div_id = 'all_'+resolved_table
    header_columns = career_table_headers[resolved_table]
    team_column = find_team_column(header_columns)

    return div_id, header_columns, team_column

def parse_a_players_career_table(page, table):
    tree = html.fromstring(page)
    div_id, header_columns, team_column = get_divid_headercolumns(table)

    rows = get_table_rows(tree, div_id)
    parsed_rows = [parse_row_given_header_column(row, header_columns) \
        for row in rows if row[team_column].text_content() != "TOT"]
    
    return parsed_rows
