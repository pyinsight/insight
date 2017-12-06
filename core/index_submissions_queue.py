"""
Takes the Reddit redis submission queue and indexes them into the ElasticSearch server.
Before indexing, each submission is associated with a sentiment score, via `link_to_sentiment.py'.
"""
#!/usr/bin/env python
import elasticsearch as es
import json
import praw
import time
from datetime import datetime, timedelta
from utils.redisqueue import RedisQueue
from link_to_sentiment import SubmissionSentimizer
from secrets import REDDIT_CREDENTIALS


def create_submissions_index(client):
    submission_mapping = {
        'submission': {
            'properties': {
                'author': {'type': 'text'},
                'created_utc': {
                    'type': 'date',
                    'format': 'epoch_second',
                },
                'domain': {
                    'type': 'text',
                },
                'downs': {
                    'type': 'integer',
                },
                'id': {
                    'type': 'text',
                },
                'num_comments': {
                    'type': 'integer',
                },
                'score': {
                    'type': 'integer',
                },
                'selftext': {
                    'type': 'text',
                },
                'sentiment': {
                    'type': 'float',
                },
                'subreddit': {
                    'type': 'text',
                },
                'subreddit_id': {
                    'type': 'text',
                },
                'thumbnail': {
                    'type': 'text',
                },
                'title': {
                    'type': 'text',
                },
                'ups': {
                    'type': 'integer',
                },
                'url': {
                    'type': 'text',
                }
            }
        }
    }

    body = {'mappings': submission_mapping}

    try:
        print('Creating submission index')
        es_client.indices.create(index='reddit', body=body)
    except es.exceptions.TransportError as e:
        if e.error != 'index_already_exists_exception':
            raise


def index_submission(es_client, submission):
    try:
        print(f'Indexing {submission["score"]}--{submission["title"]}')
        submission['created_utc'] = int(submission['created_utc'])
        print(submission['thumbnail'])
        es_client.index(index='reddit', doc_type='submission', id=submission['id'], body=submission)
    except (ValueError, IndexError, es.ElasticsearchException) as e:
        print(e)
        pass


def main(es_client, queue):
    """Pulls submissions from redis queue once they are a day old"""
    ss = SubmissionSentimizer()
    ONE_DAY = timedelta(1)
    while True:
        if queue.qsize() == 0:
            print(f'Queue empty {datetime.utcnow()}')
            time.sleep(1)  # avoid excessive checks
            continue
        submission = json.loads(queue.front())
        submission_created_dt = datetime.fromtimestamp(submission['created_utc'])
        time_diff = datetime.utcnow() - submission_created_dt  # TimeDelta of time elapsed between submission and now
        if False: #time_diff < ONE_DAY:
            print(f'Sleeping until {submission_created_dt + ONE_DAY}')
            time.sleep(int(time_diff.total_seconds() + 1))  # sleep until the front of the queue becomes a day old
            continue
        # retrieve sentiment score and index into ElasticSearch
        submission['sentiment'] = ss.get_sentiment(f'https://reddit.com/{submission["id"]}')
        index_submission(es_client, submission)
        queue.get()  # remove submission from queue, as it has been indexed


if __name__ == '__main__':
    es_client = es.Elasticsearch()
    reddit = praw.Reddit(
        user_agent=REDDIT_CREDENTIALS['user_agent'],
        client_id=REDDIT_CREDENTIALS['user_id'],
        client_secret=REDDIT_CREDENTIALS['client_secret'],
        username=REDDIT_CREDENTIALS['username'],
        password=REDDIT_CREDENTIALS['password'])
    queue = RedisQueue('reddit-submissions-queue')
    if not es_client.indices.exists(index="reddit"):
        create_submissions_index(es_client)
    main(es_client, queue)


