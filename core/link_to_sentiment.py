import praw
import nltk
from secrets import REDDIT_CREDENTIALS
from nltk.classify import NaiveBayesClassifier

nltk.download('punkt')

class Comment:

    """Comment class to store and calculate the sentiment of the comment"""

    def __init__(self, text, classifier):
        self.text = text
        self.sentiment = "none"
        self.classifier = classifier

        """calls sentiment calculation for the comment text"""

        self.calculate_sentiment()

    """gets the sentiment of the comment"""

    def calculate_sentiment(self):
        self.sentiment = self.classifier.classify(format_sentence(self.text))

    """turns comment object into a string"""

    def __str__(self):
        return u' '.join((self.sentiment, self.text)).encode('utf-8').strip()


class Thread:

    """Thread object to store and look up comments to be processed"""

    def __init__(self, link, reddit_object, classifier):
        self.link = link
        self.comments = []
        self.reddit = reddit_object
        self.submission = reddit.submission(url=link)
        self.classifier = classifier
        self.average = 0.0

    """gets each comment from the thread based on the link"""

    def get_comments(self):
        self.submission.comments.replace_more(limit=None)
        for comment in self.submission.comments.list():
            self.comments.append(Comment(comment.body, self.classifier))

    """prints all comments stored in thread currently"""

    def print_comments(self):
        for comment in self.comments:
            print(comment)

    """average the positivity or negativity of the whole thread"""

    def average_sentiments(self):

        total = 0.0
        num_of_comments = 0

        for comment in self.comments:
            num_of_comments += 1

            if comment.sentiment is "pos":
                total += 1

        average = total / num_of_comments

        return average


def format_sentence(sent):
    """tokenizes the reddit comment"""
    return({word: True for word in nltk.word_tokenize(sent)})


def setup_classifier():
    """set up classifier and train it with the dater"""
    pos = []
    with open("./pos-list.txt") as f:
        for i in f:
            pos.append([format_sentence(i), 'pos'])

    neg = []
    with open("./neg-list.txt") as f:
        for i in f:
            neg.append([format_sentence(i), 'neg'])

    training = pos[:int((.8)*len(pos))] + neg[:int((.8)*len(neg))]
    test = pos[int((.8)*len(pos)):] + neg[int((.8)*len(neg)):]

    return NaiveBayesClassifier.train(training)

if __name__ == '__main__':

    link = "https://www.reddit.com/r/wholesomebpt/comments/7hbjj0/just_marry_him_already/"

    reddit = praw.Reddit(user_agent=REDDIT_CREDENTIALS['user_agent'],
                        client_id=REDDIT_CREDENTIALS['user_id'],
                        client_secret=REDDIT_CREDENTIALS['client_secret'],
                        username=REDDIT_CREDENTIALS['username'],
                        password=REDDIT_CREDENTIALS['password'])

    submission = reddit.submission(url=link)

    classifier = setup_classifier()

    """gets all comments from the given link"""

    threads = Thread(link, reddit, classifier)
    threads.get_comments()

    #print(threads.print_comments())

    print(threads.average_sentiments())

