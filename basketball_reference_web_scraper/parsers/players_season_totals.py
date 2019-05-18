# from lxml import html

from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM, POSITION_ABBREVIATIONS_TO_POSITION
from basketball_reference_web_scraper.parsers.common import COLUMN_RENAMER, COLUMN_PARSER, \
    find_team_column, parse_souped_row_given_header_columns, split_header_columns, get_all_tables_with_soup

__totals_stats_by_year_header_string = "Player,Pos,Age,Tm,G,GS,MP,FG,FGA,FG%,3P,3PA,3P%,2P,2PA,2P%,eFG%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS"
_totals_stats_by_year_header_columns = split_header_columns(__totals_stats_by_year_header_string)

def parse_players_season_totals(page, skip_totals=False):
    all_tables = get_all_tables_with_soup(page)

    rows = all_tables['PLAYER TOTALS TABLE']
    header_columns = _totals_stats_by_year_header_columns

    if skip_totals:
        team_column = find_team_column(header_columns)
        return [parse_souped_row_given_header_columns(row, header_columns)
            for row in rows if (row[team_column].text != "TOT" and len(row[0].text))]
    else:
        return [parse_souped_row_given_header_columns(row, header_columns) 
            for row in rows]
