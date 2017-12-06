import argparse
import elasticsearch as es
import csv
import sys
import os
from glob import glob
from link_to_sentiment import SubmissionSentimizer
from utils.elasticsearch_utils import create_submissions_index


FIELDS_TO_KEEP = [
    'author', 'created_utc', 'domain', 'downs', 'id', 'num_comments',
    'score', 'selftext', 'subreddit', 'subreddit_id', 'thumbnail', 'title', 'ups', 'url'
]

NON_NULLABLE_FIELDS = [
    'author', 'created_utc', 'id', 'subreddit', 'title', 'url'
]

NUMERIC_FIELDS = [
    'created_utc', 'downs', 'num_comments', 'score', 'ups'
]


def coerce_to_int(val):
    """ Coerce val to int, returns None if unable to """
    try:
        return int(val)
    except ValueError:
        return None


def create_arg_parser():
    """"Creates and returns the ArgumentParser object."""

    parser = argparse.ArgumentParser(description='Description of your app.')
    parser.add_argument('dataDirectory', help='Path to the data directory containing the csv files.')
    return parser


def index_submission(es_client, submission_doc):
    """ Indexes the submission into the elasticsearch reddit index """
    try:
        print(f'Indexing {submission_doc["score"]}--{submission_doc["title"]}')
        es_client.index(index='reddit', doc_type='submission', id=submission_doc['id'], body=submission_doc)
    except (ValueError, IndexError, es.ElasticsearchException) as e:
        print(e)
        pass


def index_submissions_csv_file(csvfile, es_client, sub_sentimizer):
    """
    Indexes the `csvfile` by prearing each line to a document compatible with the elasticsearch submission schema.
    """
    csvreader = csv.reader(csvfile)
    # read in header and map property names to their respective indexes
    index_of = {prop: index for index, prop in enumerate(next(csvreader))}
    for i, line in enumerate(csvreader):
        doc = {field: line[index_of[field]] for field in FIELDS_TO_KEEP}
        if not all((doc[field] for field in NON_NULLABLE_FIELDS)):
            # print('Skipping doc: {doc}', file=sys.stderr)
            continue
        for field in NUMERIC_FIELDS:
            doc[field] = coerce_to_int(doc[field])
        doc['sentiment'] = sub_sentimizer.get_sentiment(f'https://reddit.com/{doc["id"]}')
        index_submission(es_client, doc)


def main():
    """ Indexes each submissions csv file in `base_data_dir` to elasticsearch """
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    if not os.path.exists(parsed_args.dataDirectory):
        print(parsed_args.dataDirectory)
        print('Please enter a valid data directory')
        sys.exit(1)

    es_client = es.Elasticsearch()
    sub_sentimizer = SubmissionSentimizer()  # expensive to setup, so only do once
    if not es_client.indices.exists(index="reddit"):
        create_submissions_index(es_client)

    datapath_pattern = os.path.join(parsed_args.dataDirectory, '*.csv')
    # glob finds all pathnames matching specified datapath_pattern
    for csv_path in glob(datapath_pattern):
        with open(csv_path) as csvfile:
            index_submissions_csv_file(csvfile, es_client, sub_sentimizer)


if __name__ == '__main__':
    main()
