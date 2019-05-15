from lxml import html

from basketball_reference_web_scraper.data  import TEAM_ABBREVIATIONS_TO_TEAM, COLUMN_RENAMER, COLUMN_PARSER


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

build_keys = lambda outkey, list:  [(item, outkey) for item in list]
__base_table_renamer = dict(
    build_keys('per_game', __per_game_names) + 
    build_keys('totals', __totals_names) + 
    build_keys('per_minute', __per_minute_names) + 
    build_keys('per_poss', __per_poss_names) + 
    build_keys('advanced', __advanced_names) + 
    build_keys('shooting', __shooting_names) + 
    build_keys('pbp', __pbp_names))

__playoff_career_table_renamer = dict([('playoffs_'+k, 'playoffs_'+v) for (k, v) in __base_table_renamer.items()])

VALID_CAREER_TABLE_NAMES = __base_career_tables + __playoff_career_tables + __game_high_names
_career_table_renamer = {**__base_table_renamer, **__playoff_career_table_renamer, 
    **dict(build_keys('year-and-career-highs', __game_high_names))}

UNIQUE_CAREER_TABLES = list(set(_career_table_renamer.values()))

def split_header_columns(header_string):
    return header_string.split(",")

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
__playoff_career_table_headers = dict([('playoffs_'+k, v) for (k, v) in __base_career_table_headers.items()])
_career_table_headers = {**__base_career_table_headers, **__playoff_career_table_headers}

def get_table_rows(tree, div_id):
    divs = tree.xpath('//div[@id="{div_id}"]'.format(div_id=div_id))
    if len(divs) != 1:
        raise IOError("Got incorrect number of divs for {div_id} (expected 1, got {num_divs}".format(
            table=table, num_divs=len(divs)))

    div = divs[0]

    ## grab all table rows within this div, since I've already trimmed the page down to the div I want
    rows = div.xpath('//table/tbody/tr')
    return rows

def parse_player_career_stats_row(row, header_columns):
    """
    parse a single row given a list of column names

    leverages COLUMN_RENAMER and COLUMN_PARSER to get output names
    and the datatype of each column
    """

    to_return = {"slug":  str(row[1].get("data-append-csv"))}
    for ii, key in enumerate(header_columns):
        if header_columns[ii] != 'empty':
            to_return[COLUMN_RENAMER[key]] = COLUMN_PARSER[key](row[ii].text_content())
    return to_return

def find_team_column(header_columns):
    return header_columns.index('Tm')


def get_divid_headercolumns(table):
    """
    get the id string to search for in the page and the headers for a table
    """
    if table not in _career_table_renamer:
        msg = "Don't know how to get table {table}.  Must be one of: ".format(table=table)
        msg += ' '.join(list(_career_table_renamer.keys()))
        raise KeyError(msg)

    resolved_table = _career_table_renamer[table]
    
    div_id = 'all_'+resolved_table
    header_columns = _career_table_headers[resolved_table]
    team_column = find_team_column(header_columns)

    return div_id, header_columns, team_column


def parse_a_players_career_table(page, table):
    tree = html.fromstring(page)
    div_id, header_columns, team_column = get_divid_headercolumns(table)

    rows = get_table_rows(tree, div_id)
    parsed_rows = [parse_player_career_stats_row(row, header_columns) \
        for row in rows if row[team_column].text_content() != "TOT"]
    
    return parsed_rows
