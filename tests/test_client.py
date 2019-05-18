import tempfile

from basketball_reference_web_scraper import client

__user_agent_list = [   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

### this is hardly a comprehensive test suite.  
## for now, I just want to make sure all the calls 
## work on a zero-th order level when I make changes
## to the general structure (broadly speaking,
## I've checked the column parsing by hand, and 
## won't bother doing that here

## going to be a bunch of calls, so let's slow down
## our request rate a bit (and mess with the user agent)
def wait_random_time(max_wait_seconds=3.14159*1.5):
    import random
    import time
    ### wait some period of time and set a new user agent string
    seconds_to_wait = random.random()*max_wait_seconds
    time.sleep(seconds_to_wait)
    client.http_client.USER_AGENT = random.choice(__user_agent_list)

_tempdir = tempfile.gettempdir()

def run_test(function, args, kwargs):
    function(*args, **kwargs)
    print(f"Succesfully ran client.{function.__name__} with\n\targs = {args}\n\tkwargs = {kwargs}\n")
    wait_random_time()

### -> list of function, args, kwargs to run a test with:
test_list = [
    ### do all the options of the yearly ones work?
    ## totals:
    (client.players_season_totals, (2018, ), 
        dict(output_type='csv', output_file_path=_tempdir+'/test.csv')),

    (client.players_season_totals, (2018, ), 
        dict(skip_totals=True, output_type='json', output_file_path=_tempdir+'/test.json')),

    (client.players_season_totals, (2018, ), dict(playoffs=True)), 

    ## advanced
    (client.players_advanced_stats, (2018, ), 
        dict(output_type='csv', output_file_path=_tempdir+'/test.csv')),

    (client.players_advanced_stats, (2018, ), 
        dict(skip_totals=True, output_type='json', output_file_path=_tempdir+'/test.json')),

    (client.players_advanced_stats, (2018, ), dict(playoffs=True)), 

    ### what about a long time ago?
    (client.players_season_totals, (1950, ), 
        dict(output_type='json', output_file_path=_tempdir+'/test.json')),

    (client.players_season_totals, (1950,), 
        dict(playoffs=True, output_type='csv', output_file_path=_tempdir+'/test.csv')),

    (client.players_advanced_stats, (1950,), {}),

    (client.players_advanced_stats, (1950,), dict(playoffs=True)), 

    ## what about schedules?
    (client.season_schedule, (2018,), {}),

    ## what about career tables (for different tables)
    (client.single_player_career_tables, ('jamesle01', ), 
        dict(output_type='csv', output_file_path=_tempdir+'/test')),

    (client.single_player_career_tables, ('jamesle01', ), 
        dict(tables='all', output_type='csv', output_file_path=_tempdir+'/test')),

    (client.single_player_career_tables, ('jamesle01', ), 
        dict(tables='pergame', output_type='csv', output_file_path=_tempdir+'/test.csv')),

    (client.single_player_career_tables, ('jamesle01', ), 
        dict(tables=['pergame', 'per 36', 'game highs', 'shooting'])),

    ### what about playoffs on a series by series basis
    (client.all_playoffs_series_in_one_year, (2017, ),
        dict(output_type='csv', output_directory=_tempdir)),

    (client.all_playoffs_series_in_one_year, (1950, ),
        dict(output_type='json', output_directory=_tempdir)),

    (client.all_playoffs_series_in_one_year, (2018, ), 
        dict(tables='basic')),

    ## do box scores work?
    (client.player_box_scores, (15, 1, 2019),
        dict(output_type='json', output_file_path=_tempdir+'/test.json')),

    (client.team_box_scores, (15, 1, 2019), {}),
]


for function, args, kwargs in test_list:
    run_test(function, args, kwargs)


