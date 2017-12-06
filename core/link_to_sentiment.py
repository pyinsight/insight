import praw
import nltk
from secrets import REDDIT_CREDENTIALS
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('punkt')
nltk.download('vader_lexicon')

class Comment:

    """Comment class to store and calculate the sentiment of the comment"""

    def __init__(self, text, score, classifier):
        self.text = text
        self.sentiment = None
        self.classifier = classifier
        self.score = score

        self.neg_sentiment = 0.0
        self.pos_sentiment = 0.0
        self.over_sentiment = 0.0

        """calls sentiment calculation for the comment text"""

        self.calculate_sentiment()

    """gets the sentiment of the comment"""

    def calculate_sentiment(self):
        sentiment_scores = self.classifier.polarity_scores(self.text)

        self.neg_sentiment = sentiment_scores['neg']
        self.pos_sentiment = sentiment_scores['pos']
        self.over_sentiment = sentiment_scores['compound']

    """gets the upvotes of the comment object"""

    def get_score(self):
        return self.score

    """turns comment object into a string"""

    def __str__(self):
        return u' '.join((self.sentiment, self.text)).encode('utf-8').strip()


class Thread:

    """Thread object to store and look up comments to be processed"""

    def __init__(self, link, reddit_object, classifier):
        self.link = link
        self.comments = []
        self.reddit = reddit_object
        self.submission = self.reddit.submission(url=link)
        self.classifier = classifier
        self.average = 0.0
        self.title = self.submission.title

    """gets each comment from the thread based on the link"""

    def get_comments(self):
        self.submission.comments.replace_more(limit=100)
        for comment in self.submission.comments:
            # possibly change this to only count if count has a positive score
            self.comments.append(Comment(comment.body, comment.score, self.classifier))


    """prints all comments stored in thread currently"""

    def print_comments(self):
        for comment in self.comments:
            print(comment)

    """gets the average positivity of negativity of the thread title
        returns 0 if neg
        returns 1 if pos
    """

    def get_title_sentiment(self):
        title_sentiment = self.classifier.polarity_scores(self.title)
        return title_sentiment['compound']

    """average the positivity or negativity of the whole thread"""

    def average_sentiments(self):
        if self.submission.num_comments == 0:
            return None

        total = 0.0
        total_score = 0

        for comment in self.comments:
            total += comment.over_sentiment

        # get comment average sentiment
        
        average_comments = total / len(self.comments)

        # title sentiment
        
        title_sentiment = self.get_title_sentiment()


        # total sentiment with title weighed as 50% of the average sentimentn of the post
        
        total_sentiment = title_sentiment * .5 + average_comments * .5

        return total_sentiment * 1000


def format_sentence(sent):
    """tokenizes the reddit comment"""
    return({word: True for word in nltk.word_tokenize(sent)})


def setup_classifier():
    """set up classifier and train it with the dater"""

    return SentimentIntensityAnalyzer()


class SubmissionSentimizer:
    """Simple class that allows sentiment analysis on reddit posts"""
    def __init__(self):
        self.classifier = setup_classifier()

        self.reddit = praw.Reddit(
            user_agent=REDDIT_CREDENTIALS['user_agent'],
            client_id=REDDIT_CREDENTIALS['user_id'],
            client_secret=REDDIT_CREDENTIALS['client_secret'],
            username=REDDIT_CREDENTIALS['username'],
            password=REDDIT_CREDENTIALS['password'])

    def get_sentiment(self, url):
        threads = Thread(url, self.reddit, self.classifier)
        threads.get_comments()
        return threads.average_sentiments()


if __name__ == '__main__':

    link = "https://www.reddit.com/r/television/comments/7hsy5f/terry_crews_sues_wme_agent_adam_venit_for_sexual/"
    ss = SubmissionSentimizer()
    
    print(ss.get_sentiment(link))



