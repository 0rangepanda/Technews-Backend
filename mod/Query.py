from google.cloud import bigquery
import os

def hacker_news_query(start_time, end_time, LIMIT, URL=True, TITLE=True):
    client = bigquery.Client()
    QUERY = (
        'SELECT title,url '
        'FROM `bigquery-public-data.hacker_news.full` '
        'WHERE time between %d and %d '
        'and type=\'story\''
        ) % (start_time, end_time, )

    if URL:
        QUERY += 'and not url=\'\''
    if TITLE:
        QUERY += 'and not title=\'\''
    if LIMIT>0:
        QUERY += 'LIMIT %d'%LIMIT

    print QUERY

    TIMEOUT = 30  # in seconds
    query_job = client.query(QUERY)  # API request - starts the query

    # Waits for the query to finish
    iterator = query_job.result(timeout=TIMEOUT)
    rows = list(iterator)
    assert query_job.state == 'DONE'
    return rows
