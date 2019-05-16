import requests
import warnings
import copy
import os

from basketball_reference_web_scraper import http_client
from basketball_reference_web_scraper import output

from basketball_reference_web_scraper.errors import InvalidSeason, InvalidDate, InvalidPlayer
from basketball_reference_web_scraper.json_encoders import BasketballReferenceJSONEncoder


def player_box_scores(day, month, year, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    try:
        values = http_client.player_box_scores(day=day, month=month, year=year)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidDate(day=day, month=month, year=year)
        else:
            raise http_error
    return output.output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=output.box_scores_to_csv,
        encoder=BasketballReferenceJSONEncoder,
        json_options=json_options,
    )





def season_schedule(season_end_year, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    try:
        values = http_client.season_schedule(season_end_year)
    except requests.exceptions.HTTPError as http_error:
        # https://github.com/requests/requests/blob/master/requests/status_codes.py#L58
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidSeason(season_end_year=season_end_year)
        else:
            raise http_error
    return output.output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=output.schedule_to_csv,
        encoder=BasketballReferenceJSONEncoder,
        json_options=json_options,
    )

def playoff_series_list(playoffs_year, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    """
    get the list of playoff series that happened in the playoffs of a given year

    returns a list of rows with entries 'series_name', 'winning_team', 'losing_team', 
    'series_score', 'stats_link_ending'
    """
    if playoffs_year == 1954:
        raise ValueError("Can't parse the round-robin playoff schedule of 1954, sorry")

    try:
        values = http_client.playoffs_series(playoffs_year)
    except requests.exceptions.HTTPError as http_error:
        # https://github.com/requests/requests/blob/master/requests/status_codes.py#L58
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidSeason(season_end_year=playoffs_year)
        else:
            raise http_error
    return output.output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=output.playoff_series_to_csv,
        encoder=BasketballReferenceJSONEncoder,
        json_options=json_options,
    )


def player_career_tables(player_id, tables=['totals', 'advanced'], 
    output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    """
    get one or more tables of a players career (one line per season)

    Args:
        player_id (str):  A valid Basketball-Reference.com Player ID.
                          Can be read from the CSV style tables on 
                          Basketball-Reference.com as the portion of a
                          player's name column following the "/"

        tables (list-like):  A list of tables to pull out of the 
    """
    if tables in ['all', 'All', 'ALL']:
        from basketball_reference_web_scraper.parsers.player_career import UNIQUE_CAREER_TABLES
        tables = UNIQUE_CAREER_TABLES
    if isinstance(tables, str):
        tables = [tables]

    try:
        values_list = http_client.player_career(player_id, tables)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidPlayer(player_id=player_id)
        else:
            raise http_error

    if output_file_path is not None and len(tables) > 1:
        if output_file_path.endswith('.csv'):
            output_file_path = output_file_path[:-4]
        output_file_path_list = [output_file_path+'_{table}.csv'.format(table=table) for table in tables]
    else:
        output_file_path_list = [output_file_path] * len(tables)
    return {table: output.output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=output.players_career_writer,
        encoder=BasketballReferenceJSONEncoder,
        json_options=json_options,
        table=table,
    ) for (table, values, output_file_path) in zip(tables, values_list, output_file_path_list)}


def playoff_series_stats(playoff_series, tables=['basic', 'advanced'], 
    output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    """
    get basic and/or advanced stats from a given playoff series

    Args:
        playoff_series (dict-like):  a lookup table containing (at least)
                                     'winning_team', 'losing_team', 
                                     'winning_team_games_won', 
                                     'losing_team_games_won', and
                                     'stats_link_ending' (i.e. an 
                                     element in a list returned by 
                                     `func:playoff_series_list`.  
                                     the first two should be of the 
                                     `Team` class, and the last 
                                     should point to a page containing 
                                     the stats for a given playoff series 
                                     between those two teams (when 
                                     appended to the end of the 
                                     BASE_URL), e.g., 
                                     playoffs/2016-nba-finals-cavaliers-vs-warriors.html

        tables (list-like):  A list of tables to pull out of the page.
                             either 'basic', 'advanced', or both.
    """
    if isinstance(tables, str):
        tables = [tables]

    year = int(playoff_series['stats_link_ending'].split('/')[-1].split('-')[0])
    if year <= 1983 and 'advanced' in tables:
        warnings.warn("Cannot get advanced stats for playoffs series before 1984")
        tables = ['basic']
        if isinstance(output_file_path, str) and not output_file_path.endswith('.csv'):
            output_file_path = [output_file_path + '_basic.csv']


    try:
        values_list = http_client.playoff_series_stats(playoff_series, tables)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidSeries(series=playoff_series)
        else:
            raise http_error

    if isinstance(output_file_path, list):
        assert len(output_file_path) >= len(tables), "must provide an output file for all tables if making by hand"
        output_file_path_list = output_file_path
    elif output_file_path is not None and len(tables) > 1:
        if output_file_path.endswith('.csv'):
            output_file_path = output_file_path[:-4]
        output_file_path_list = [output_file_path+'_{table}.csv'.format(table=table) for table in tables]
    else:
        output_file_path_list = [output_file_path] * len(tables)
        
    return {table: output.output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=output.playoff_stats_writer,
        encoder=BasketballReferenceJSONEncoder,
        json_options=json_options,
        table=table,
    ) for (table, values, output_file_path) in zip(tables, values_list, output_file_path_list)}


def players_season_totals(season_end_year, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    try:
        values = http_client.players_season_totals(season_end_year)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidSeason(season_end_year=season_end_year)
        else:
            raise http_error
    return output.output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=output.players_season_totals_to_csv,
        encoder=BasketballReferenceJSONEncoder,
        json_options=json_options,
    )


def playoffs_series_in_one_year(year, tables=['basic', 'advanced'], output_type=None, 
        output_directory=None, output_write_option=None, json_options=None):
    """
    download the list of playoff series in a year then download the stats from each of those series
    """
    kwargs = dict(output_type=output_type, output_write_option=output_write_option, json_options=json_options)

    if output_directory is not None:
        if not output_directory.endswith('/'):  
            output_directory += '/'

        if str(year) not in os.path.abspath(output_directory):
            output_base = output_directory + f'{year}'
        else:
            output_base = output_directory

        schedule_output_path = output_base + 'playoff_schedule.csv'
    else:
        assert save_schedule == False, "cannot save schedule without an output directory"
        assert output_type is not None, "must set output_type as well as output_directory to save files"

    series_list = playoff_series_list(year, output_file_path=schedule_output_path, **kwargs)

    series_count = {}
    for series in series_list:
        round_name = series['series_name']
        finals = 'finals' in round_name.lower()
        if True in [round_name.startswith(f'{x}') for x in ['Western', 'Central', 'Eastern']]:
            finals = False
        if 'semi' in round_name.lower():
            finals = False

        if round_name in series_count:
            unique_series_name = round_name + '_{}'.format(series_count[round_name])
            series_count[round_name] = series_count[round_name] + 1
        elif finals:
            unique_series_name = copy.deepcopy(round_name)
        else:
            unique_series_name = round_name + '_0'
            series_count[round_name] = 1
        
        series['round_name'] = round_name
        series['unique_series_name'] = unique_series_name

    if output_directory is not None:
        output_file_path_list = [output_base + series['unique_series_name'] for series in series_list]
    else:
        output_file_path_list = [None] * len(series_list)
    return {series['unique_series_name']: playoff_series_stats(series, tables, output_file_path=output_file_path, **kwargs)
        for (series, output_file_path) in zip(series_list, output_file_path_list)}


def team_box_scores(day, month, year, output_type=None, output_file_path=None, output_write_option=None, json_options=None):
    try:
        values = http_client.team_box_scores(day=day, month=month, year=year)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidDate(day=day, month=month, year=year)
        else:
            raise http_error
    return output.output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=output.team_box_scores_to_csv,
        encoder=BasketballReferenceJSONEncoder,
        json_options=json_options,
    )


def players_advanced_stats(season_end_year,output_type=None,output_file_path=None,output_write_option=None,json_options=None):
    try:
        values = http_client.player_advanced_stats(season_end_year)
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == requests.codes.not_found:
            raise InvalidSeason(season_end_year=season_end_year)
        else:
            raise http_error
    return output.output(
        values=values,
        output_type=output_type,
        output_file_path=output_file_path,
        output_write_option=output_write_option,
        csv_writer=output.players_advanced_to_csv,
        encoder=BasketballReferenceJSONEncoder,
        json_options=json_options,
    )
