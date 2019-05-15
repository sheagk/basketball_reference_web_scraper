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

def get_rows_headercolumns(all_tables, table, team):
    """
    get the id string to search for in the page and the headers for a table
    """
    team_name = team.value
    decap_team_name = ' '.join([word[0].upper() + word[1:].lower() for word in team_name.split()])+' '

    if table == 'advanced':
        header_columns = _playoff_advanced_header_columns
        table_id = decap_team_name + 'Advanced Stats Table'
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
        header_columns = _playoff_basic_header_columns
        table_id = decap_team_name + 'Basic Stats Table'
        rows = all_tables[table_id]

        ### the following does work, since the basic tables aren't commented out, but I'm not doing it 
        ## anymore because it only works for basic tables
        # rows = tree.xpath('//table[@id="'+table_id+'"]/tbody/tr')

    return rows, header_columns

def parse_playoff_series_stats(page, winning_team, losing_team, table):
    assert table in ['basic', 'advanced'], \
        "must provide either 'basic' or 'advanced' for table; gave {table}".format(table)

    # soup = BeautifulSoup(page, 'html.parser')
    all_tables = get_all_tables_with_soup(page)
    winning_rows, header_columns = get_rows_headercolumns(all_tables, table, winning_team)

    parsed_rows = []
    for row in winning_rows:
        prow = parse_souped_row_given_header_columns(row, header_columns)
        prow['team'] = winning_team.value
        parsed_rows.append(prow)

    losing_rows, header_columns = get_rows_headercolumns(all_tables, table, losing_team)

    for row in losing_rows:
        prow = parse_souped_row_given_header_columns(row, header_columns)
        prow['team'] = losing_team.value
        parsed_rows.append(prow)

    return parsed_rows
