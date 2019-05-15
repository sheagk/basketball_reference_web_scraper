from basketball_reference_web_scraper.data import COLUMN_RENAMER, COLUMN_PARSER

def parse_row_given_header_column(row, header_columns):
    """
    parse a single row given a list of column names

    leverages COLUMN_RENAMER and COLUMN_PARSER to get output names
    and the datatype of each column
    """

    to_return = {"slug":  str(row[1].get("data-append-csv"))}
    for ii, key in enumerate(header_columns):
        if header_columns[ii] != 'empty':
            to_return[COLUMN_RENAMER[key]] = COLUMN_PARSER[key](row[ii].text_content())
    return to_return

def find_team_column(header_columns):
    return header_columns.index('Tm')

def split_header_columns(header_string):
    return header_string.split(",")