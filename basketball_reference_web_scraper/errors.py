class InvalidDate(Exception):
    def __init__(self, day, month, year):
        message = "Date with year set to {year}, month set to {month}, and day set to {day} is invalid"\
            .format(
                year=year,
                month=month,
                day=day,
            )
        super().__init__(message)


class InvalidSeason(Exception):
    def __init__(self, season_end_year):
        message = "Season end year of {season_end_year} is invalid".format(season_end_year=season_end_year)
        super().__init__(message)

class InvalidPlayer(Exception):
    def __init__(self, player_id):
        message = "Player ID of {player_id} is invalid".format(player_id=player_id)
        super().__init__(message)

class InvalidSeries(Exception):
    def __init__(self, series):
        message = "No series between {winning_team} and {losing_team} exists at {series_address}".format(
            winning_team=series['winning_team'].value,
            losing_team=series['losing_team'].value,
            series_address=series['stats_link_ending'])
        super().__init__(message)