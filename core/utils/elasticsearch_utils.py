import elasticsearch as es

def create_submissions_index(es_client):
    submission_mapping = {
        'submission': {
            'properties': {
                'author': {'type': 'text'},
                'created_utc': {
                    'type': 'date',
                    'format': 'epoch_second',
                },
                'domain': {
                    'type': 'text',
                },
                'downs': {
                    'type': 'integer',
                },
                'id': {
                    'type': 'text',
                },
                'num_comments': {
                    'type': 'integer',
                },
                'score': {
                    'type': 'integer',
                },
                'selftext': {
                    'type': 'text',
                },
                'sentiment': {
                    'type': 'float',
                },
                'subreddit': {
                    'type': 'text',
                },
                'subreddit_id': {
                    'type': 'text',
                },
                'thumbnail': {
                    'type': 'text',
                },
                'title': {
                    'type': 'text',
                },
                'ups': {
                    'type': 'integer',
                },
                'url': {
                    'type': 'text',
                }
            }
        }
    }

    body = {'mappings': submission_mapping}

    try:
        print('Creating submission index')
        es_client.indices.create(index='reddit', body=body)
    except es.exceptions.TransportError as e:
        if e.error != 'index_already_exists_exception':
            raise
