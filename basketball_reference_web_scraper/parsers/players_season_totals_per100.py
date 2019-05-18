from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM, POSITION_ABBREVIATIONS_TO_POSITION
from basketball_reference_web_scraper.parsers.common import COLUMN_RENAMER, COLUMN_PARSER, \
    find_team_column, parse_souped_row_given_header_columns, split_header_columns, get_all_tables_with_soup

__totals_stats_per100_by_year_header_string = "Player,Pos,Age,Tm,G,GS,MP,FGperposs,FGAperposs,FG%,3Pperposs,3PAperposs,3P%,2Pperposs,2PAperposs,2P%,FTperposs,FTAperposs,FT%,ORBperposs,DRBperposs,TRBperposs,ASTperposs,STLperposs,BLKperposs,TOVperposs,PFperposs,PTSperposs,empty,ORtg,DRtg"
_totals_stats_per100_by_year_header_columns = split_header_columns(__totals_stats_per100_by_year_header_string)

def parse_players_season_totals_per100(page, skip_totals=False):
    all_tables = get_all_tables_with_soup(page)

    rows = all_tables['PLAYER PER 100 POSS TABLE']
    header_columns = _totals_stats_per100_by_year_header_columns

    if skip_totals:
        team_column = find_team_column(header_columns)
        return [parse_souped_row_given_header_columns(row, header_columns)
            for row in rows if (row[team_column].text != "TOT" and len(row[0].text))]
    else:
        return [parse_souped_row_given_header_columns(row, header_columns) 
            for row in rows]
