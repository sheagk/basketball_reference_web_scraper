from lxml import html

from basketball_reference_web_scraper.data  import TEAM_NAME_TO_TEAM
from basketball_reference_web_scraper.parsers.player_career import get_table_rows
from basketball_reference_web_scraper.utilities import str_to_str, str_to_int

def parse_series_list_row(row):
    ## skip blank rows between the rounds
    if row.text_content() == '':
        return None

    ## skip the togglable game-by-game rows
    elif 'Game 1' in row.text_content():
        return None

    print(row.text_content())

    series_name = str_to_str(row[0].text_content())
    teams_string = str_to_str(row[1].text_content())

    winning_team = str_to_str(teams_string.split('over')[0])
    losing_team = str_to_str(teams_string.split('over')[1].strip().split('\n')[0])
    
    winning_team = TEAM_NAME_TO_TEAM.get(winning_team.upper())
    losing_team = TEAM_NAME_TO_TEAM.get(losing_team.upper())

    record = teams_string.split('(')[-1].split(')')[0]
    winning_team_games_won = str_to_int(record.split('-')[0])
    losing_team_games_won = str_to_int(record.split('-')[1])

    if losing_team_games_won > winning_team_games_won:
        winning_team_games_wonwinning_team_games_won, losing_team_games_won = losing_team_games_won, winning_teams_games_won

    stats_link_ending = row[2].findall('a')[0].values()[0] 

    return {
        "series_name": str_to_str(row[0].text_content()),
        "winning_team": winning_team, 
        "losing_team": losing_team,
        "winning_team_games_won": winning_team_games_won,
        "losing_team_games_won": losing_team_games_won,
        "stats_link_ending": stats_link_ending,
    }

def parse_playoff_series_list(page):
    tree = html.fromstring(page)
    rows = tree.xpath('//table[@id="all_playoffs"]/tbody/tr')

    parsed_rows = [parse_series_list_row(row) for row in rows]
    return [row for row in parsed_rows if row is not None]

