from lxml import html
from bs4 import BeautifulSoup

from basketball_reference_web_scraper.data import TEAM_NAME_TO_TEAM
from basketball_reference_web_scraper.utilities import str_to_str
from basketball_reference_web_scraper.parsers.common import get_all_tables_with_soup, \
    parse_souped_row_given_header_columns, split_header_columns, COLUMN_PARSER, COLUMN_RENAMER

__team_box_score_header_string = "MP,FG,FGA,FG%,3P,3PA,3P%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,+/-"
_team_box_score_header_columns = split_header_columns(__team_box_score_header_string)

def parse_team_total(footer, team):
    row = footer.xpath('tr/td')
    to_return = {}

    for ii, key in enumerate(_team_box_score_header_columns):
        if key == 'Player':
            to_return['player_id'] = row[ii].get('data-append-csv')
            to_return['player_name'] = str_to_str(row[ii].text_content())
        elif key == 'empty':
            continue
        else:
            to_return[COLUMN_RENAMER[key]] = COLUMN_PARSER[key](row[ii].text_content())
    return to_return

def parse_team_totals(page):
    """
    gets only the totals for a team from the box score of a game
    (i.e. the last row)
    """
    soup = BeautifulSoup(page, features='lxml')
    scorebox = soup.find('div', {'class':'scorebox'})
    teams = [TEAM_NAME_TO_TEAM(item.text) for item in 
        scorebox.find_all('a', {'itemprop':'name'})]

    tree = html.fromstring(page)
    tables = tree.xpath('//table[contains(@class, "stats_table")]')
    footers = [
        footer
        for table in tables
        if "basic" in table.attrib["id"]
        for footer in table.xpath("tfoot")
    ]
    return [
        parse_team_total(footer=footer, team=teams[footers.index(footer)])
        for footer in footers
    ]
