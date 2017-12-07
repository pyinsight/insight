import praw
from utils.redisqueue import RedisQueue
from secrets import REDDIT_CREDENTIALS


SUBREDDITS = [
    'uncensorednews', 'news', 'worldnews', 'politics', 'upliftingnews', 'truenews',
    'worldpolitics', 'business', 'technology', 'stocks', 'investing', 'euro'
]


def enqueue_submissions():
    reddit = praw.Reddit(
        user_agent=REDDIT_CREDENTIALS['user_agent'],
        client_id=REDDIT_CREDENTIALS['user_id'],
        client_secret=REDDIT_CREDENTIALS['client_secret'],
        username=REDDIT_CREDENTIALS['username'],
        password=REDDIT_CREDENTIALS['password']
    )

    submission_queue = RedisQueue('reddit-submissions-queue')
    # pause_after < 0 yields None after every request, allowing you to control what happens before asking for more
    for i, submission in enumerate(reddit.subreddit('+'.join(SUBREDDITS)).stream.submissions(pause_after=-1)):
        if submission is None:
            continue
        submission_queue.put(submission.id)
        if (i + 1) % 50 == 0:
            print(f'Queue Size: {submission_queue.qsize()}')


if __name__ == '__main__':
    enqueue_submissions()
