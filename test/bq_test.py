from google.cloud import bigquery
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/roger/Documents/code/Python/BigQuery/python2/My Project 68452-ae0ad4fc4ab7.json"


def query_test():
    client = bigquery.Client()
    QUERY = (
        #'SELECT DAYOFYEAR(pickup_datetime) AS daynumber '
        'SELECT pickup_datetime AS daynumber '
        'FROM `bigquery-public-data.new_york.tlc_green_trips_2015` '
        'LIMIT 10'
        )

    TIMEOUT = 30  # in seconds
    query_job = client.query(QUERY)  # API request - starts the query
    #assert query_job.state == 'RUNNING'
    print(dir(query_job))
    #
    # print(query_job.use_legacy_sql)
    # query_job.use_legacy_sql = True

    # Waits for the query to finish
    iterator = query_job.result(timeout=TIMEOUT)
    rows = list(iterator)

    assert query_job.state == 'DONE'
    return rows


def hacker_news_query(start_time, end_time, LIMIT):
    client = bigquery.Client()
    QUERY = (
        'SELECT title,url '
        'FROM `bigquery-public-data.hacker_news.full` '
        'WHERE time between %d and %d '
        'and type=\'story\' and not title=\'\''
        'LIMIT %d'
        ) % (start_time, end_time, LIMIT, )
    print QUERY

    TIMEOUT = 30  # in seconds
    query_job = client.query(QUERY)  # API request - starts the query

    # Waits for the query to finish
    iterator = query_job.result(timeout=TIMEOUT)
    rows = list(iterator)
    assert query_job.state == 'DONE'
    return rows

#rows = query_test()
rows = hacker_news_query(1351623092,1468446826,10)
print rows
