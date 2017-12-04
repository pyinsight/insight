import praw
import json
from utils.redisqueue import RedisQueue
from secrets import REDDIT_CREDENTIALS


def insert_submissions():
    reddit = praw.Reddit(
        user_agent=REDDIT_CREDENTIALS['user_agent'],
        client_id=REDDIT_CREDENTIALS['user_id'],
        client_secret=REDDIT_CREDENTIALS['client_secret'],
        username=REDDIT_CREDENTIALS['username'],
        password=REDDIT_CREDENTIALS['password']
    )

    fields_to_keep = [
        'author', 'created_utc', 'domain', 'downs', 'id', 'num_comments',
        'score', 'selftext', 'subreddit', 'subreddit_id', 'thumbnail', 'title', 'ups', 'url'
    ]
    submission_queue = RedisQueue('reddit-submissions-queue')
    # pause_after < 0 yields None after every request allowing you to control what happens before asking for more
    for i, submission in enumerate(reddit.subreddit('all').stream.submissions(pause_after=-1)):
        if submission is None:
            continue
        submission_fields = vars(submission)
        # Coerce two fields for JSON serialization compatibility
        submission_fields['subreddit'] = submission_fields['subreddit'].display_name
        submission_fields['author'] = submission_fields['author'].name
        # filter down submission to just the fields in elasticsearch schema
        submission_fields_filtered = {field: submission_fields[field] for field in fields_to_keep}
        submission_json_str = json.dumps(submission_fields_filtered)
        # enqueue the submission to the redis queue
        submission_queue.put(submission_json_str)
        if (i+1) % 50 == 0:
            print(f'Queue Size: {submission_queue.qsize()}')


if __name__ == '__main__':
    insert_submissions()
