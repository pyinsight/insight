"""
Takes the Reddit redis submission queue and indexes them into the ElasticSearch server.
Before indexing, each submission is associated with a sentiment score, via `link_to_sentiment.py'.
"""
import elasticsearch as es
import requests
import time
from datetime import datetime, timedelta
from utils.redisqueue import RedisQueue
from utils.elasticsearch_utils import create_submissions_index
from submission_ext import SubmissionExt


FIELDS_TO_INDEX = [
    'author', 'created_utc', 'domain', 'downs', 'id', 'num_comments',
    'score', 'selftext', 'sentiment', 'subreddit', 'subreddit_id', 'thumbnail', 'title', 'ups', 'url'
]


def index_submission(es_client, submission_dict):
    try:
        print(f'Indexing {submission_dict["score"]}--{submission_dict["title"]}')
        submission_dict['created_utc'] = int(submission_dict['created_utc'])
        es_client.index(index='reddit', doc_type='submission', id=submission_dict['id'], body=submission_dict)
    except (ValueError, IndexError, es.ElasticsearchException) as e:
        print(e)
        pass


def main(es_client, queue):
    """Pulls submissions from redis queue once they are a day old"""
    ONE_DAY = timedelta(1)
    while True:
        if queue.qsize() == 0:
            print(f'Queue empty {datetime.utcnow()}')
            time.sleep(1)  # avoid excessive checks
            continue
        submission_id = queue.front().decode('utf-8')
        try:
            submission = SubmissionExt(id=submission_id)
        except requests.exceptions.RequestException:
            queue.get()  # skip problematic posts (most likely deleted)
        submission_created_dt = datetime.fromtimestamp(submission.created_utc)
        time_diff = datetime.utcnow() - submission_created_dt  # TimeDelta of time elapsed between submission and now
        if False:  # time_diff < ONE_DAY:
            print(f'Sleeping until {submission_created_dt + ONE_DAY}')
            time.sleep(int(time_diff.total_seconds() + 1))  # sleep until the front of the queue becomes a day old
            continue
        index_submission(es_client, submission.to_dict(FIELDS_TO_INDEX))
        queue.get()  # remove submission from queue, as it has been indexed


if __name__ == '__main__':
    es_client = es.Elasticsearch()
    queue = RedisQueue('reddit-submissions-queue')
    if not es_client.indices.exists(index="reddit"):
        create_submissions_index(es_client)
    main(es_client, queue)
