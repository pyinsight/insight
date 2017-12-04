import praw
import json
import time
from utils.redisqueue import RedisQueue
from secrets import REDDIT_CREDENTIALS


def insert_posts():
    reddit = praw.Reddit(
        user_agent=REDDIT_CREDENTIALS['user_agent'],
        client_id=REDDIT_CREDENTIALS['user_id'],
        client_secret=REDDIT_CREDENTIALS['client_secret'],
        username=REDDIT_CREDENTIALS['username'],
        password=REDDIT_CREDENTIALS['password']
    )

    fields_to_keep = ['domain', 'subreddit', 'selftext', 'likes', 'id', 'view_count', 'title', 'pinned', 'score', 'subreddit_id', 'downs',
          'created', 'url', 'created_utc', 'ups', 'media', 'num_comments', 'thumbnail']

    post_queue = RedisQueue('reddit-post-queue')
    # pause_after < 0 yields None after every request allowing you to control what happens before asking for more
    for i, post in enumerate(reddit.subreddit('all').stream.submissions(pause_after=-1)):
        if post is None:
            continue
        post_fields = vars(post)
        post_fields['subreddit'] = post_fields['subreddit'].display_name  # for JSON serialization
        post_fields_filtered = {field: post_fields[field] for field in fields_to_keep}
        post_json = json.dumps(post_fields_filtered)
        # enqueue the post to index, temporary workaround to avoid excessive growth
        if i % 30 == 0:
            post_queue.put(post_json)
            print(f'Queue Size: {post_queue.qsize()}')


if __name__ == '__main__':
    insert_posts()


