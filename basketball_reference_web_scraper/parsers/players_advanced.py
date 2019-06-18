# from lxml import html

from basketball_reference_web_scraper.utilities import str_to_str, str_to_float, str_to_int
from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM, POSITION_ABBREVIATIONS_TO_POSITION
from basketball_reference_web_scraper.parsers.common import COLUMN_RENAMER, COLUMN_PARSER, \
    find_team_column, parse_souped_row_given_header_columns, split_header_columns, get_all_tables_with_soup

__advanced_stats_by_year_header_string = "Player,Pos,Age,Tm,G,MP,PER,TS%,3PAr,FTr,ORB%,DRB%,TRB%,AST%,STL%,BLK%,TOV%,USG%,empty,OWS,DWS,WS,WS/48,empty,OBPM,DBPM,BPM,VORP"
_advanced_stats_by_year_header_columns = split_header_columns(__advanced_stats_by_year_header_string)

def parse_players_advanced_stats(page, skip_totals=False):
    all_tables = get_all_tables_with_soup(page)

    rows = all_tables['ADVANCED TABLE']
    header_columns = _advanced_stats_by_year_header_columns

    if skip_totals:
        team_column = find_team_column(header_columns)
        return [parse_souped_row_given_header_columns(row, header_columns)
            for row in rows if (row[team_column].text != "TOT" and len(row[0].text))]
    else:
        return [parse_souped_row_given_header_columns(row, header_columns)
            for row in rows]
