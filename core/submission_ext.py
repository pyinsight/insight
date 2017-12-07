import praw
from secrets import REDDIT_CREDENTIALS
from nltk.sentiment.vader import SentimentIntensityAnalyzer


NON_NULLABLE_FIELDS = [
    'author', 'created_utc', 'id', 'subreddit', 'title', 'url'
]

def is_valid_submission(submission):
    _ = submission.title
    fields_dict = vars(submission)
    for field in NON_NULLABLE_FIELDS:
        if field not in fields_dict or fields_dict[field] in ['', None]:
            return False
    return True


class SubmissionExt(praw.models.Submission):
    """
    Small child class of praw.models.Submission that provides a sentiment score attribute
    All other funcitonality is the same, documented at:
        `https://praw.readthedocs.io/en/latest/code_overview/models/submission.html`
    """

    # Static class variables that are common across all instances of this class
    sia = SentimentIntensityAnalyzer()
    reddit = praw.Reddit(
        user_agent=REDDIT_CREDENTIALS['user_agent'],
        client_id=REDDIT_CREDENTIALS['user_id'],
        client_secret=REDDIT_CREDENTIALS['client_secret'],
        username=REDDIT_CREDENTIALS['username'],
        password=REDDIT_CREDENTIALS['password'])

    def __init__(self, url=None, id=None):
        super().__init__(SubmissionExt.reddit, url=url, id=id)  # will raise if id and url are None
        if not is_valid_submission(self):
            print(f'https://reddit.com/{self.id}')
            raise ValueError("Submission is broken")
        self.sentiment = self._calculate_sentiment()

    def __repr__(self):
        return f'SubmissionExt(id={self.id}, sentiment={self.sentiment})'

    def __str__(self):
        return f'SubmissionExt(id={self.id}, sentiment={self.sentiment})'

    def to_dict(self, fields_to_keep):
        """
        Returns a dictionary representaiton of this instance, whose keys are denoted by `fields_to_keep`
        This is used for indexing a submission into ElasticSearch
        """
        fields_dict = vars(self)
        # Coerce complex fields to their string representations
        if not isinstance(fields_dict['subreddit'], str):
            fields_dict['subreddit'] = fields_dict['subreddit'].display_name
        if not isinstance(fields_dict['author'], str):
            fields_dict['author'] = fields_dict['author'].name if fields_dict['author'] else 'deleted'
        fields_dict['created_utc'] = int(fields_dict['created_utc'])
        # filter down submission to just the fields in elasticsearch schema
        fields_dict_filtered = {field: fields_dict[field] for field in fields_to_keep}
        return fields_dict_filtered

    def _calculate_comments_sentiment(self):
        sum_, count = 0, 0
        self.comments.replace_more(limit=None)  # necessary to loop through all comments
        for comment in self.comments.list():
            sentiment = SubmissionExt.sia.polarity_scores(comment.body)['compound']
            sum_ += sentiment
            count += 1
        return sum_ / count if count > 0 else 0

    def _calculate_sentiment(self):
        """
        Averages the sentiment of the title with the aggregate sentiment of the comments
        Returns a float from -1 to 1, where -1 is extremely negative, 0 neutral, and 1 extremely positive.
        All sentiments are calculated via VADER (see http://comp.social.gatech.edu/papers/icwsm14.vader.hutto.pdf)
        """
        comments_sentiment = self._calculate_comments_sentiment()
        title_sentiment = SubmissionExt.sia.polarity_scores(self.title)['compound']
        return (comments_sentiment + title_sentiment) / 2


if __name__ == '__main__':
    url = 'https://www.reddit.com/r/redditdev/comments/6wddne/accessing_a_submission_or_comment_by_id_only/'
    ss = SubmissionExt(url)
    print(ss)
