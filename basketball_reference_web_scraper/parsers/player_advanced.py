from lxml import html

from basketball_reference_web_scraper.data import TEAM_ABBREVIATIONS_TO_TEAM, POSITION_ABBREVIATIONS_TO_POSITION


def parse_player_advanced_stats(row):
    return {
        "name": str(row[1].text_content()),
        "positions": parse_positions(row[2].text_content()),
        "age": int(row[3].text_content()),
        "team": TEAM_ABBREVIATIONS_TO_TEAM[row[4].text_content()],
        "games_played": int(row[5].text_content()),
        "minutes_played": int(row[6].text_content()),
        "player_efficiency_rating": row[7].text_content(),
        "true_shooting_percent": row[8].text_content(),
        "three_point_attempt_rate": row[9].text_content(),
        "free_throw_attempt_rate": row[10].text_content(),
        "offensive_rebound_pct": row[11].text_content(),
        "defensive_rebound_pct": row[12].text_content(),
        "total_rebound_pct": row[13].text_content(),
        "assists_pct": row[14].text_content(),
        "steals_pct": row[15].text_content(),
        "blocks_pct": row[16].text_content(),
        "turnover_pct": row[17].text_content(),
        "usage_pct": row[18].text_content(),
        "offensive_win_shares": row[20].text_content(),
        "defensive_win_shares": row[21].text_content(),
        "total_win_shares": row[22].text_content(),
        "offensive_bpm": row[25].text_content(),
        "defensive_bpm": row[26].text_content(),
        "total_bpm": row[27].text_content(),
        "vorp": row[28].text_content(),
    }


def parse_players_advanced_stats(page):
    tree = html.fromstring(page)
    print("gotpage")
    # Basketball Reference includes individual rows for players that played for multiple teams in a season
    # These rows have a separate class ("italic_text partial_table") than the players that played for a single team
    # across a season.
    rows = tree.xpath('//table[@id="advanced_stats"]/tbody/tr[contains(@class, "full_table") or contains(@class, "italic_text partial_table") and not(contains(@class, "rowSum"))]')
    totals = []
    for row in rows:
        # Basketball Reference includes a "total" row for players that got traded
        # which is essentially a sum of all player team rows
        # I want to avoid including those, so I check the "team" field value for "TOT"
        if row[4].text_content() != "TOT":
            totals.append(parse_player_advanced_stats(row))
    return totals


def parse_positions(positions_content):
    return list(map(lambda position_abbreviation: POSITION_ABBREVIATIONS_TO_POSITION[position_abbreviation],
                    positions_content.split("-")))
