import logging

from flask import Flask
from flask import request
from flask import jsonify

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from google.cloud import videointelligence

STORAGE_NAME = 'user-videos'
LABELS_DATABASE_NAME = 'generated-labels'
AUTH_FILE = 'video-storytelling-adi-firebase-adminsdk-72km3-5a560f013a.json'

cred = credentials.Certificate(AUTH_FILE)
firebase_admin.initialize_app(cred, {
		'databaseURL': 'https://' + LABELS_DATABASE_NAME + '.firebaseio.com/'
	})


app = Flask(__name__)


@app.route('/')
def hello():

	video_file_path = request.args.get('video_file_path')

	if video_file_path == None or len(video_file_path) == 0:
		logging.info('no path parameter provided')
		# print('no path parameter provided')
		return 'no path parameter provided'


	path = 'gs://' + STORAGE_NAME + '/' + video_file_path
	logging.info('Accessing video from ' + path + ' ...')
	# print('Accessing video from ' + path + ' ...')

	video_client = videointelligence.VideoIntelligenceServiceClient()
	features = [videointelligence.enums.Feature.LABEL_DETECTION]
	mode = videointelligence.enums.LabelDetectionMode.SHOT_AND_FRAME_MODE
	config = videointelligence.types.LabelDetectionConfig(label_detection_mode=mode)
	context = videointelligence.types.VideoContext(label_detection_config=config)

	operation = video_client.annotate_video(path, features=features, video_context=context)
	
	logging.info('Processing video for labelling...')
	# print('Processing video for labelling...')

	result = operation.result(timeout=180)

	labels = []

	# Process video/segment level label annotations
	segment_labels = result.annotation_results[0].segment_label_annotations
	for i, segment_label in enumerate(segment_labels):
		labels.append(segment_label.entity.description)

	# Process shot level label annotations
	shot_labels = result.annotation_results[0].shot_label_annotations
	for i, shot_label in enumerate(shot_labels):
		labels.append(shot_label.entity.description)

	# # Process frame level label annotations
	# frame_labels = result.annotation_results[0].frame_label_annotations
	# for i, frame_label in enumerate(frame_labels):
	# 	labels.append(frame_label.entity.description)

	labels = list(set(labels))
	logging.info(labels)
	# print(labels)

	if len(labels) == 0:
		labels.append('please wait')

	trimmed_file_path = video_file_path.split('.')[0]

	ref = db.reference(trimmed_file_path)
	ref.set(labels)
	logging.info('Written to ' + LABELS_DATABASE_NAME)
	# print('Written to ' + LABELS_DATABASE_NAME)

	return jsonify(labels)


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