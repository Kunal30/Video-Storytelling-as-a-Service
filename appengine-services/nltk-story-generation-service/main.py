import logging

from flask import Flask
from flask import request
from flask import jsonify

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from randomsentence.sentence_maker import SentenceMaker
from randomsentence.sentence_tools import SentenceTools

STORIES_DATABASE_NAME = 'generated-stories'
AUTH_FILE = 'video-storytelling-adi-firebase-adminsdk-72km3-5a560f013a.json'

cred = credentials.Certificate(AUTH_FILE)
firebase_admin.initialize_app(cred, {
		'databaseURL': 'https://' + STORIES_DATABASE_NAME + '.firebaseio.com/'
	})


app = Flask(__name__)


@app.route('/')
def hello():

	labels = request.args.get('labels')
	video_file_path = request.args.get('video_file_path')

	if video_file_path == None or len(video_file_path) == 0 or labels == None or len(labels) == 0:
		logging.info('Wrong or Empty Query parameters to the Sentence Generator Module')
		# print('Wrong or Empty Query parameters to the Sentence Generator Module')
		return 'Wrong or Empty Query parameters to the Sentence Generator Module'

	labels = labels.split(",")
	output = str()
	sentences = []

	if labels[0] == 'please wait' and len(labels) == 1:
		output = 'Please try again'
	else:
		sentence_maker = SentenceMaker()
		tagged_sentence = sentence_maker.from_keyword_list(labels)
		sentence_tools = SentenceTools()
		output = sentence_tools.detokenize_tagged(tagged_sentence)

	logging.info(output)
	# print(output)

	sentences.append(output)

	ref = db.reference(video_file_path)
	ref.set(sentences)
	logging.info('Written to ' + STORIES_DATABASE_NAME)
	# print('Written to ' + STORIES_DATABASE_NAME)

	return jsonify(output)


@app.errorhandler(500)  
def server_error(e):
	logging.info(e)
	# print(e)
	logging.exception('An error occurred during a request.')
	return """
	An internal error occurred: <pre>{}</pre>
	See logs for full stacktrace.
	""".format(e), 500


if __name__ == '__main__':
	# This is used when running locally. Gunicorn is used to run the
	# application on Google App Engine. See entrypoint in app.yaml.

	app.run(host='127.0.0.1', port=8080, debug=True)