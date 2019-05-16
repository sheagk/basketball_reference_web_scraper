from bs4 import BeautifulSoup
from copy import deepcopy

from basketball_reference_web_scraper.utilities import merge_two_dicts
from basketball_reference_web_scraper.data  import TEAM_ABBREVIATIONS_TO_TEAM, TEAM_TO_TEAM_ABBREVIATIONS
from basketball_reference_web_scraper.parsers.common import COLUMN_RENAMER, COLUMN_PARSER, \
     find_team_column, parse_souped_row_given_header_columns, split_header_columns, get_all_tables_with_soup

## only two tables, and they're just "basic" and "advanced", so no aliases (or dictionaries) needed/allowed here
__playoff_basic_header_string = "Player,Age,G,GS,MP,FG,FGA,3P,3PA,FT,FTA,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,FG%,3P%,FT%,MPpg,PTSpg,TRBpg,ASTpg,STLpg,BLKpg"
_playoff_basic_header_columns = split_header_columns(__playoff_basic_header_string)

__playoff_advanced_header_string = "Player,Age,G,GS,MP,TS%,eFG%,ORB%,DRB%,TRB%,AST%,STL%,BLK%,TOV%,USG%,ORtg,DRtg,GmSc"
_playoff_advanced_header_columns = split_header_columns(__playoff_advanced_header_string)

__old_playoff_basic_header_string = "Player,Age,G,MP,FG,FGA,3P,3PA,FT,FTA,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,FG%,3P%,FT%,MPpg,PTSpg,TRBpg,ASTpg,STLpg,BLKpg"
_old_playoff_basic_header_columns = split_header_columns(__old_playoff_basic_header_string)

def get_rows_headercolumns(all_tables, table, team, team_record):
    """
    get the id string to search for in the page and the headers for a table
    """
    team_name = deepcopy(team.value)

    if table == 'advanced':
        header_columns = _playoff_advanced_header_columns
        table_id = team_name + ' Advanced Stats Table'.upper()
        rows = all_tables[table_id]

        ## this doesn't work because the advanced tables (and non-basic tables on career stats pages)
        ## are commented out in the source code for some reason.  because of that, I've switched over
        ## to bs4, where I can parse those comments anyway (see get_all_tables_with_soup)
        # divs = tree.xpath('//div[@id="'+table_id+'"]')
        # if len(divs) != 1:
        #     raise IOError("Got incorrect number of divs for {table_id} (expected 1, got {num_divs})".format(
        #         table_id=table_id, num_divs=len(divs)))        
        # div = divs[0]
        # rows = div.xpath('//table/tbody/tr')

    else:
        table_id = team_name + ' Basic Stats Table'.upper()
        old_table_id = team_name + ' ' + team_record + ' Table'.upper()
        
        if table_id in all_tables:
            header_columns = _playoff_basic_header_columns
            rows = all_tables[table_id]
        elif old_table_id in all_tables:
            ### search for the older (pre-1984) captioned tables
            ## note that there are no advanced stats for those years anyway
            header_columns = _old_playoff_basic_header_columns
            rows = all_tables[old_table_id]               
        else:
            raise KeyError(f"Can't find {table_id} or {old_table_id} on page.  Available tables are:\n\t"+"; ".join(all_tables.keys()))

        ## the following _does_ work (since the basic tables aren't commented out) 
        ## but I'm not doing it anymore anyways because it **only** works for basic 
        ## tables
        # rows = tree.xpath('//table[@id="'+table_id+'"]/tbody/tr')

    return rows, header_columns

def parse_playoff_series_stats(page, series, table):
    assert table in ['basic', 'advanced'], \
        f"must provide either 'basic' or 'advanced' for table; gave {table}"

    # soup = BeautifulSoup(page, 'html.parser')
    all_tables = get_all_tables_with_soup(page)

    winning_team = series['winning_team']
    losing_team = series['losing_team']
    winning_record = '({0}-{1})'.format(
        series['winning_team_games_won'],
        series['losing_team_games_won'])

    losing_record = '({1}-{0})'.format(
        series['winning_team_games_won'],
        series['losing_team_games_won'])

    winning_rows, header_columns = get_rows_headercolumns(all_tables, table, winning_team, winning_record)

    parsed_rows = []
    for row in winning_rows:
        prow = parse_souped_row_given_header_columns(row, header_columns)
        prow['team'] = winning_team.value
        parsed_rows.append(prow)

    losing_rows, header_columns = get_rows_headercolumns(all_tables, table, losing_team, losing_record)

    for row in losing_rows:
        prow = parse_souped_row_given_header_columns(row, header_columns)
        prow['team'] = losing_team.value
        parsed_rows.append(prow)

    return parsed_rows
