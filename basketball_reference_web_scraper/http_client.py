import requests

from basketball_reference_web_scraper.errors import InvalidDate
from basketball_reference_web_scraper.parsers.box_scores.players import parse_player_box_scores
from basketball_reference_web_scraper.parsers.box_scores.games import parse_game_url_paths
from basketball_reference_web_scraper.parsers.box_scores.teams import parse_team_totals
from basketball_reference_web_scraper.parsers.schedule import parse_schedule, parse_schedule_for_month_url_paths
from basketball_reference_web_scraper.parsers.players_season_totals import parse_players_season_totals
from basketball_reference_web_scraper.parsers.player_advanced import parse_players_advanced_stats
from basketball_reference_web_scraper.parsers.playoffs_series_list import parse_playoff_series_list
from basketball_reference_web_scraper.parsers.playoff_series_stats import parse_playoff_series_stats
from basketball_reference_web_scraper.parsers.player_career import parse_a_players_career_table

BASE_URL = 'https://www.basketball-reference.com'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'

def player_career(player_id, tables=['totals', 'advanced']):
    if isinstance(tables, str):
        tables = [tables]

    tables = [table.lower() for table in tables]

    first_init = player_id[0]
    url = '{BASE_URL}/players/{first_init}/{player_id}.html'.format(
        BASE_URL=BASE_URL,
        first_init=first_init,
        player_id=player_id)

    response = requests.get(url=url, headers={'User-Agent': USER_AGENT})

    response.raise_for_status()

    return [parse_a_players_career_table(response.content, table) for table in tables]



def player_box_scores(day, month, year):
    url = '{BASE_URL}/friv/dailyleaders.cgi?month={month}&day={day}&year={year}'.format(
        BASE_URL=BASE_URL,
        day=day,
        month=month,
        year=year
    )

    response = requests.get(url=url, 
        allow_redirects=False, headers={'User-Agent': USER_AGENT})

    response.raise_for_status()

    if response.status_code == requests.codes.ok:
        return parse_player_box_scores(response.content)

    raise InvalidDate(day=day, month=month, year=year)


def schedule_for_month(url):
    response = requests.get(url=url, headers={'User-Agent': USER_AGENT})

    response.raise_for_status()

    return parse_schedule(response.content)


def season_schedule(season_end_year):
    url = '{BASE_URL}/leagues/NBA_{season_end_year}_games.html'.format(
        BASE_URL=BASE_URL,
        season_end_year=season_end_year
    )

    response = requests.get(url=url, headers={'User-Agent': USER_AGENT})

    response.raise_for_status()

    season_schedule_values = parse_schedule(response.content)
    other_month_url_paths = parse_schedule_for_month_url_paths(response.content)

    for month_url_path in other_month_url_paths:
        url = '{BASE_URL}{month_url_path}'.format(BASE_URL=BASE_URL, month_url_path=month_url_path)
        monthly_schedule = schedule_for_month(url=url)
        season_schedule_values.extend(monthly_schedule)

    return season_schedule_values


def playoffs_series(playoffs_year):
    url = '{BASE_URL}/playoffs/NBA_{playoffs_year}.html'.format(
        BASE_URL=BASE_URL,
        playoffs_year=playoffs_year
    )

    response = requests.get(url=url, headers={'User-Agent': USER_AGENT})

    response.raise_for_status()

    return parse_playoff_series_list(response.content)


def playoff_series_stats(playoff_series, tables=['basic', 'advanced']):
    url = '{BASE_URL}/{series_path}'.format(
        BASE_URL=BASE_URL,
        series_path=playoff_series['stats_link_ending'],
    )

    response = requests.get(url=url, headers={'User-Agent': USER_AGENT})

    response.raise_for_status()

    return [parse_playoff_series_stats(response.content, playoff_series, table) 
        for table in tables]


def players_season_totals(season_end_year):
    url = '{BASE_URL}/leagues/NBA_{season_end_year}_totals.html'.format(
        BASE_URL=BASE_URL,
        season_end_year=season_end_year,
    )

    response = requests.get(url=url, headers={'User-Agent': USER_AGENT})

    response.raise_for_status()

    return parse_players_season_totals(response.content)


def team_box_score(game_url_path):
    url = "{BASE_URL}/{game_url_path}".format(BASE_URL=BASE_URL, game_url_path=game_url_path)

    response = requests.get(url=url, headers={'User-Agent': USER_AGENT})

    response.raise_for_status()

    return parse_team_totals(response.content)


def team_box_scores(day, month, year):
    url = "{BASE_URL}/boxscores/".format(BASE_URL=BASE_URL)

    response = requests.get(url=url, 
        params={"day": day, "month": month, "year": year},
        headers={'User-Agent': USER_AGENT})

    response.raise_for_status()

    game_url_paths = parse_game_url_paths(response.content)

    return [
        box_score
        for game_url_path in game_url_paths
        for box_score in team_box_score(game_url_path=game_url_path)
    ]


def player_advanced_stats(season_end_year):
    url = '{BASE_URL}/leagues/NBA_{season_end_year}_advanced.html'.format(
        BASE_URL=BASE_URL,
        season_end_year=season_end_year,
    )

    response = requests.get(url=url, headers={'User-Agent': USER_AGENT})

    response.raise_for_status()

    return parse_players_advanced_stats(response.content)
