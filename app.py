import elasticsearch as es
from collections import defaultdict
from flask import Flask, render_template, request
from elasticsearch_dsl import Search

app = Flask(__name__)
es_client = es.Elasticsearch()


def simple_search(q):
    s = Search(using=es_client, index='reddit') \
        .query('match', title=q)[:100]
    resp = s.execute()
    return resp['hits']['hits']


@app.route('/')
def index():
    return render_template('search.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('q')
    hits = simple_search(query)
    return render_template('results.html',
                           hits=hits,
                           subreddits=top_subreddits(hits))


def top_subreddits(hits):
    """ Returns (subreddit, freq) pairs that the hits were in, sorted by frequency"""
    subreddit_freqs = defaultdict(int)
    for hit in hits:
        subreddit_freqs[hit['_source']['subreddit']] += 1
    # sort by freqs descending
    top_subreddits = sorted(subreddit_freqs.items(), key=lambda t: t[1], reverse=True)
    return top_subreddits
