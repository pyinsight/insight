import elasticsearch as es
from collections import defaultdict
from datetime import datetime
from flask import Flask, render_template, request
from elasticsearch_dsl import Search

app = Flask(__name__)
es_client = es.Elasticsearch()


@app.route('/')
def index():
    return render_template('search.html')


@app.route('/search', methods=['GET', 'POST'])
def results():
    query = request.args.get('q')
    hits = simple_search(query)
    return render_template('results.html', hits=hits, subreddits=top_subreddits(hits))


def simple_search(q):
    s = Search(using=es_client, index='reddit') \
        .query('match', title=q)[:100]
    resp = s.execute()
    return resp['hits']['hits']


def top_subreddits(hits):
    """ Returns (subreddit, freq) pairs that the hits were in, sorted by frequency"""
    subreddit_freqs = defaultdict(int)
    for hit in hits:
        subreddit_freqs[hit['_source']['subreddit']] += 1
    # sort by freqs descending
    top_subreddits = sorted(subreddit_freqs.items(), key=lambda t: t[1], reverse=True)
    return top_subreddits


def days_hours_minutes(td):
    return td.days, td.seconds // 3600, (td.seconds // 60) % 60


@app.template_filter('epoch')
def format_epoch(t):
    """ Formats the unix epoch to a user-friendly string denoting how much time has passed since `t` """
    submission_dt = datetime.fromtimestamp(t)
    today = datetime.utcnow()
    delta = today - submission_dt
    days, hours, minutes = days_hours_minutes(delta)
    if days:
        return f'{days} day{"s" if days > 1 else ""} ago'
    if hours:
        return f'{hours} hour{"s" if hours > 1 else ""} ago'
    return f'{minutes} minute{"s" if minutes > 1 else ""} ago'


@app.template_filter('sentiment')
def format_sentiment(s):
    if s is None:
        return 'No sentiment available'
    if (0.25 >= s >= -0.25):
        ret = 'Neutral'
    elif s <= -.25:
        if s <= -.65:
            ret = 'Confidently negative'
        else:
            ret = 'Negative'
    else:
        if s >= .65:
            ret = 'Confidently positive'
        else:
            ret = 'Positive'
    ret += f' ({s:.2f})'
    return ret
