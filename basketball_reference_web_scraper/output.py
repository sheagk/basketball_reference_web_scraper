import csv
import json
import copy
import warnings

from basketball_reference_web_scraper.data import OutputType, OutputWriteOption
from basketball_reference_web_scraper.utilities import merge_two_dicts

box_score_fieldname = [
    "player_id",
    "player_name",
    "team",
    "location",
    "opponent",
    "outcome",
    "seconds_played",
    "made_field_goals",
    "attempted_field_goals",
    "made_three_point_field_goals",
    "attempted_three_point_field_goals",
    "made_free_throws",
    "attempted_free_throws",
    "offensive_rebounds",
    "defensive_rebounds",
    "assists",
    "steals",
    "blocks",
    "turnovers",
    "personal_fouls",
    "game_score",
]

game_fieldname = [
    "start_time",
    "away_team",
    "away_team_score",
    "home_team",
    "home_team_score",
]

team_box_score_fieldname = [
    "team",
    "minutes_played",
    "made_field_goals",
    "attempted_field_goals",
    "made_three_point_field_goals",
    "attempted_three_point_field_goals",
    "made_free_throws",
    "attempted_free_throws",
    "offensive_rebounds",
    "defensive_rebounds",
    "assists",
    "steals",
    "blocks",
    "turnovers",
    "personal_fouls",
]

default_json_options = {
    "sort_keys": True,
    "indent": 4,
}



def output(values, output_type, output_file_path, encoder, csv_writer, 
    output_write_option=None, json_options=None, table=None):
    if output_type is None:
        ## nothing else to do or check; just return
        return values

    if output_file_path is not None and output_type is None:
        if output_file_path.endswith('.json'):
            output_type = 'json'
        elif output_file_path.endswith('.csv'):
            output_type = 'csv'
        else:
            warnings.warn("-- specified output_file_path, but it doesn't end with either .json or .csv; will not save")

    write_option = OutputWriteOption.WRITE if output_write_option is None else output_write_option

    file_written = False
    if output_type == OutputType.JSON or output_type.upper()=="JSON":
        options = default_json_options if json_options is None else merge_two_dicts(first=default_json_options, second=json_options)
        if output_file_path is None:
            json.dumps(values, cls=encoder, **options)
        else:
            with open(output_file_path, write_option.value, newline="") as json_file:
                json.dump(values, json_file, cls=encoder, **options)
        file_written = True

    if output_type == OutputType.CSV or output_type.upper()=="CSV":
        assert output_file_path is not None, "CSV output must contain a file path"
        if not output_file_path.endswith('.csv'):
            print("-- adding '.csv' to the output file path")
            output_file_path = output_file_path + '.csv'

        kwargs = dict(rows=values, output_file_path=output_file_path, write_option=write_option)
        if (csv_writer == players_career_writer) or (csv_writer == playoff_stats_writer):
            kwargs['table'] = table
        csv_writer(**kwargs)

        file_written = True

    if output_type is not None and file_written == False:
        ValueError("Unknown output type: {output_type}".format(output_type=output_type))

    return values


# I wrote the explicit mapping of CSV values because there didn't seem to be a way of outputting the values of enums
# without doing it this way


def box_scores_to_csv(rows, output_file_path, write_option):
    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=box_score_fieldname)
        writer.writeheader()
        writer.writerows(
            {
                "player_id": row["player_id"],
                "player_name": row["player_name"],
                "team": row["team"].value,
                "location": row["location"].value,
                "opponent": row["opponent"].value,
                "outcome": row["outcome"].value,
                "seconds_played": row["seconds_played"],
                "made_field_goals": row["made_field_goals"],
                "attempted_field_goals": row["attempted_field_goals"],
                "made_three_point_field_goals": row["made_three_point_field_goals"],
                "attempted_three_point_field_goals": row["attempted_three_point_field_goals"],
                "made_free_throws": row["made_free_throws"],
                "attempted_free_throws": row["attempted_free_throws"],
                "offensive_rebounds": row["offensive_rebounds"],
                "defensive_rebounds": row["defensive_rebounds"],
                "assists": row["assists"],
                "steals": row["steals"],
                "blocks": row["blocks"],
                "turnovers": row["turnovers"],
                "personal_fouls": row["personal_fouls"],
                "game_score": row["game_score"],
            } for row in rows
        )


def schedule_to_csv(rows, output_file_path, write_option):
    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=game_fieldname)
        writer.writeheader()
        writer.writerows(
            {
                "start_time": row["start_time"],
                "away_team": row["away_team"].value,
                "away_team_score": row["away_team_score"],
                "home_team": row["home_team"].value,
                "home_team_score": row["home_team_score"],
            } for row in rows
        )


def players_season_totals_to_csv(rows, output_file_path, write_option):
    from basketball_reference_web_scraper.parsers.players_season_totals import \
        _totals_stats_by_year_header_columns as header_columns
    from basketball_reference_web_scraper.parsers.common import COLUMN_RENAMER

    fieldnames = [COLUMN_RENAMER[k] for k in header_columns if k not in ['empty', 'Player']]
    if 'Player' in header_columns:
        ## put the player name and player id first
        fieldnames = ['player_id', 'player_name'] + fieldnames

    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        ## the teams are now just raw strings, so turn each row into a dictionary:
        writer.writerows(dict([(k, row[k]) for k in fieldnames]) for row in rows)

def players_advanced_to_csv(rows,output_file_path,write_option):
    from basketball_reference_web_scraper.parsers.players_advanced import \
        _advanced_stats_by_year_header_columns as header_columns

    from basketball_reference_web_scraper.parsers.common import COLUMN_RENAMER

    fieldnames = [COLUMN_RENAMER[k] for k in header_columns if k not in ['empty', 'Player']]
    if 'Player' in header_columns:
        ## put the player name and player id first
        fieldnames = ['player_id', 'player_name'] + fieldnames

    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        ## the teams are now just raw strings, so turn each row into a dictionary:
        writer.writerows(dict([(k, row[k]) for k in fieldnames]) for row in rows)

def players_season_totals_per100_to_csv(rows, output_file_path, write_option):
    from basketball_reference_web_scraper.parsers.players_season_totals_per100 import \
        _totals_stats_per100_by_year_header_columns as header_columns
    from basketball_reference_web_scraper.parsers.common import COLUMN_RENAMER

    fieldnames = [COLUMN_RENAMER[k] for k in header_columns if k not in ['empty', 'Player']]
    if 'Player' in header_columns:
        ## put the player name and player id first
        fieldnames = ['player_id', 'player_name'] + fieldnames

    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        ## the teams are now just raw strings, so turn each row into a dictionary:
        writer.writerows(dict([(k, row[k]) for k in fieldnames]) for row in rows)


def team_box_scores_to_csv(rows, output_file_path, write_option):
    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=team_box_score_fieldname)
        writer.writeheader()
        writer.writerows(
            {
                "team": row["team"].value,
                "minutes_played": row["minutes_played"],
                "made_field_goals": row["made_field_goals"],
                "attempted_field_goals": row["attempted_field_goals"],
                "made_three_point_field_goals": row["made_three_point_field_goals"],
                "attempted_three_point_field_goals": row["attempted_three_point_field_goals"],
                "made_free_throws": row["made_free_throws"],
                "attempted_free_throws": row["attempted_free_throws"],
                "offensive_rebounds": row["offensive_rebounds"],
                "defensive_rebounds": row["defensive_rebounds"],
                "assists": row["assists"],
                "steals": row["steals"],
                "blocks": row["blocks"],
                "turnovers": row["turnovers"],
                "personal_fouls": row["personal_fouls"],
            } for row in rows
        )

def playoff_series_to_csv(rows, output_file_path, write_option):
    fieldnames = ['series_name', 'winning_team', 'losing_team',
        'winning_team_games_won', 'losing_team_games_won', 'stats_link_ending']
    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(
            {
               'series_name':row['series_name'],
                "winning_team": row["winning_team"].value, 
                "losing_team": row["losing_team"].value,
                "winning_team_games_won": row["winning_team_games_won"],
                "losing_team_games_won": row["losing_team_games_won"],
                "stats_link_ending": row["stats_link_ending"],
            } for row in rows
        )

def players_career_writer(rows, output_file_path, write_option, table):
    from basketball_reference_web_scraper.parsers.player_career import career_table_headers, career_table_renamer
    from basketball_reference_web_scraper.parsers.common import COLUMN_RENAMER

    resolved_table = career_table_renamer[table]
    fieldnames = [COLUMN_RENAMER[k] for k in career_table_headers[resolved_table] if k != 'empty']

    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        ## here I've opted to store the team and positions as raw strings, so can just turn my row into a dictionary
        writer.writerows(dict([(k, row[k]) for k in fieldnames]) for row in rows)


def playoff_stats_writer(rows, output_file_path, write_option, table):
    from basketball_reference_web_scraper.parsers.common import COLUMN_RENAMER
    from basketball_reference_web_scraper.parsers.playoff_series_stats import \
        _playoff_basic_header_columns, _playoff_advanced_header_columns

    assert table in ['basic', 'advanced'], "table must be one of 'basic' or 'advanced'"

    if table == 'basic':
        header_columns = copy.deepcopy(_playoff_basic_header_columns)
        
        ## older playoff series don't keep track of games started
        if 'games_started' not in rows[0].keys():
            header_columns.pop(header_columns.index('GS'))
    else:
        header_columns = _playoff_advanced_header_columns

    ## skip empty columns and handle the player column separately, since it's turned into two
    fieldnames = [COLUMN_RENAMER[k] for k in header_columns if k not in ['empty', 'Player']]
    if 'Player' in header_columns:
        ## put the player name and player id first
        fieldnames = ['player_id', 'player_name'] + fieldnames

    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        ## again, just raw strings, so turn each row into a dictionary:
        writer.writerows(dict([(k, row[k]) for k in fieldnames]) for row in rows)


def csv_writer_from_keys(rows, output_file_path, write_option, table):
    """
    write a list of dictionaries to a file using the keys of the first row as the column headers

    all rows must have exactly the same keys.  no guarantee of column ordering,
    unless the input rows are OrderedDictionaries
    """

    fieldnames = rows[0].keys()
    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dict([(k, row[k]) for k in fieldnames]) for row in rows)

