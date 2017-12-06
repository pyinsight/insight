import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def load_json(val):
	"""reads each json object per line to data list"""

	data = []

	with open(val) as f:
		for line in f:
			data.append(json.loads(line)['body'])

	return data


def calculate_sentiment(text, classifier):
	"""returns the calculated sentiment with vader"""

	sentiment = classifier.polarity_scores(text)['compound']

	return sentiment


def calculate_sentiment_list(data, classifier):
	"""returns a tuple list of sentiments and text associated with this sentiment"""

	new_data = []

	for item in data:
		sentiment = calculate_sentiment(item, classifier)
		new_data.append({"text": item, "sentiment": sentiment})

	return new_data


if __name__ == '__main__':

	data = load_json('testmonth.json')

	sid = SentimentIntensityAnalyzer()

	sent_data = calculate_sentiment_list(data, sid)

	print(sent_data)


