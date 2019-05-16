import csv
import json

from basketball_reference_web_scraper.data import OutputType, OutputWriteOption
from basketball_reference_web_scraper.utilities import merge_two_dicts

box_score_fieldname = [
    "slug",
    "name",
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

player_season_totals_fieldname = [
    "slug",
    "name",
    "positions",
    "age",
    "team",
    "games_played",
    "games_started",
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

player_advanced_fieldname=[
        "name",
        "positions",
        "age",
        "team",
        "games_played",
        "minutes_played",
        "player_efficiency_rating",
        "true_shooting_percent",
        "three_point_attempt_rate",
        "free_throw_attempt_rate",
        "offensive_rebound_pct",
        "defensive_rebound_pct",
        "total_rebound_pct",
        "assists_pct",
        "steals_pct",
        "blocks_pct",
        "turnover_pct",
        "usage_pct",
        "offensive_win_shares",
        "defensive_win_shares",
        "total_win_shares",
        "offensive_bpm",
        "defensive_bpm",
        "total_bpm",
        "vorp"

]

default_json_options = {
    "sort_keys": True,
    "indent": 4,
}



def output(values, output_type, output_file_path, encoder, csv_writer, 
    output_write_option=None, json_options=None, table=None):
    if output_file_path is not None and output_type is None:
        print("-- specified output_file_path but no output_type")
        print("-- must give both to save file(s)")

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
                "slug": row["slug"],
                "name": row["name"],
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
    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=player_season_totals_fieldname)
        writer.writeheader()
        writer.writerows(
            {
                "slug": row["slug"],
                "name": row["name"],
                "positions": "-".join(map(lambda position: position.value, row["positions"])),
                "age": row["age"],
                "team": row["team"].value,
                "games_played": row["games_played"],
                "games_started": row["games_started"],
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


def players_advanced_to_csv(rows,output_file_path,write_option):
    with open(output_file_path, write_option.value, newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=player_advanced_fieldname)
        writer.writeheader()
        writer.writerows(
            {
                "name": row["name"],
                "positions": "-".join(map(lambda position: position.value, row["positions"])),
                "age": row["age"],
                "team": row["team"].value,
                "games_played": row["games_played"],
                "minutes_played": row["minutes_played"],
                "player_efficiency_rating": row["player_efficiency_rating"],
                "true_shooting_percent": row["true_shooting_percent"],
                "three_point_attempt_rate": row["three_point_attempt_rate"],
                "free_throw_attempt_rate": row["free_throw_attempt_rate"],
                "offensive_rebound_pct": row["offensive_rebound_pct"],
                "defensive_rebound_pct": row["defensive_rebound_pct"],
                "total_rebound_pct": row["total_rebound_pct"],
                "assists_pct": row["assists_pct"],
                "steals_pct": row["steals_pct"],
                "blocks_pct":row["blocks_pct"],
                "turnover_pct":row["turnover_pct"] ,
                "usage_pct":row["usage_pct"],
                "offensive_win_shares":row["offensive_win_shares"] ,
                "defensive_win_shares":row["defensive_win_shares"] ,
                "total_win_shares":row["total_win_shares"],
                "offensive_bpm":row["offensive_bpm"],
                "defensive_bpm":row["defensive_bpm"],
                "total_bpm":row["total_bpm"],
                "vorp":row["vorp"],
            } for row in rows
        )

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
        header_columns = _playoff_basic_header_columns
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

