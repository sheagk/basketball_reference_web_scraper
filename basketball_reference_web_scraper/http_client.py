import requests

from basketball_reference_web_scraper.errors import InvalidDate
from basketball_reference_web_scraper import parsers

BASE_URL = 'https://www.basketball-reference.com'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) ' + \
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'

def players_season_totals(season_end_year, skip_totals=False, playoffs=False):
    if playoffs:
        url = f'{BASE_URL}/playoffs/NBA_{season_end_year}_totals.html'
    else:
        url = f'{BASE_URL}/leagues/NBA_{season_end_year}_totals.html'
    response = requests.get(url=url, headers={'User-Agent': USER_AGENT})
    response.raise_for_status()
    return parsers.parse_players_season_totals(response.content)


def players_advanced_stats(season_end_year, skip_totals=False, playoffs=False):
    if playoffs:
        url = f'{BASE_URL}/playoffs/NBA_{season_end_year}_advanced.html'    
    else:
        url = f'{BASE_URL}/leagues/NBA_{season_end_year}_advanced.html'
    response = requests.get(url=url, headers={'User-Agent': USER_AGENT})
    response.raise_for_status()
    return parsers.parse_players_advanced_stats(response.content)


def player_box_scores(day, month, year):
    url = f'{BASE_URL}/friv/dailyleaders.cgi?month={month}&day={day}&year={year}'

    response = requests.get(url=url, 
        allow_redirects=False, headers={'User-Agent': USER_AGENT})

    response.raise_for_status()

    if response.status_code == requests.codes.ok:
        return parsers.parse_player_box_scores(response.content)

    raise InvalidDate(day=day, month=month, year=year)


def schedule_for_month(url):
    response = requests.get(url=url, headers={'User-Agent': USER_AGENT})

    response.raise_for_status()

    return parsers.parse_schedule(response.content)


def season_schedule(season_end_year):
    url = f'{BASE_URL}/leagues/NBA_{season_end_year}_games.html'
    response = requests.get(url=url, headers={'User-Agent': USER_AGENT})
    response.raise_for_status()

    season_schedule_values = parsers.parse_schedule(response.content)
    other_month_url_paths = parsers.parse_schedule_for_month_url_paths(response.content)

    for month_url_path in other_month_url_paths:
        url = f'{BASE_URL}{month_url_path}'
        monthly_schedule = schedule_for_month(url=url)
        season_schedule_values.extend(monthly_schedule)

    return season_schedule_values


def team_box_score(game_url_path):
    url = f"{BASE_URL}/{game_url_path}"
    response = requests.get(url=url, headers={'User-Agent': USER_AGENT})
    response.raise_for_status()
    return parsers.parse_team_totals(response.content)


def team_box_scores(day, month, year):
    url = f"{BASE_URL}/boxscores/"

    response = requests.get(url=url, 
        params={"day": day, "month": month, "year": year},
        headers={'User-Agent': USER_AGENT})

    response.raise_for_status()

    game_url_paths = parsers.parse_game_url_paths(response.content)

    return [
        box_score
        for game_url_path in game_url_paths
        for box_score in team_box_score(game_url_path=game_url_path)
    ]


def player_career(player_id, tables=['totals', 'advanced']):
    if isinstance(tables, str):
        tables = [tables]

    tables = [table.lower() for table in tables]

    first_init = player_id[0]
    url = f'{BASE_URL}/players/{first_init}/{player_id}.html'

    response = requests.get(url=url, headers={'User-Agent': USER_AGENT})

    response.raise_for_status()

    return [parsers.parse_a_players_career_table(response.content, table) 
        for table in tables]


def playoffs_series(playoffs_year):
    url = f'{BASE_URL}/playoffs/NBA_{playoffs_year}.html'
    response = requests.get(url=url, headers={'User-Agent': USER_AGENT})
    response.raise_for_status()
    return parsers.parse_playoff_series_list(response.content)


def playoff_series_stats(playoff_series, tables=['basic', 'advanced']):
    url = f"{BASE_URL}/{playoff_series['stats_link_ending']}"
    response = requests.get(url=url, headers={'User-Agent': USER_AGENT})
    response.raise_for_status()

    return [parsers.parse_playoff_series_stats(response.content, playoff_series, table) 
        for table in tables]



