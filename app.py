import elasticsearch as es
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
def hello_world():
    return render_template('search.html')

@app.route('/search', methods=['GET','POST'])
def search():
    query = request.args.get('q')
    print(query)
    hits = simple_search(query)
    print(hits[:2])
    return render_template('results.html', hits=hits)
