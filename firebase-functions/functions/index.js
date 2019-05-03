const functions = require('firebase-functions');
const admin = require('firebase-admin');
const videoIntelligence = require('@google-cloud/video-intelligence');

const request = require('request');

const PROJECT_ID = 'video-storytelling-adi'
const STORAGE_NAME = 'user-videos'
const LABELS_DATABASE_NAME = 'generated-labels'


admin.initializeApp();


exports.labelVideos = functions.storage.bucket(STORAGE_NAME).object().onFinalize(async (object) => {
	
	console.log('Requesting video-intelligence-labelling-service...');

	const link = 'https://' + PROJECT_ID + '.appspot.com/' + '?video_file_path=' + object.name;
	console.log(link);

	request.get(link, function (error, response, body) {
		if (!error && response.statusCode === 200) {
			console.log(body);
		} else {
			console.log(response.statusCode);
			console.log(error);
		}
	});

});

exports.generateStories = functions.database.instance(LABELS_DATABASE_NAME).ref('/{macAddr}/{fileName}').onCreate((snapshot, context) => {
	
	console.log('Requesting nltk-story-generation-service...');

	const labels = snapshot.val();

	const link = 'https://generate-story-dot-' + PROJECT_ID + '.appspot.com/' + '?video_file_path=' + context.params.macAddr + '/' + context.params.fileName + '&labels=' + labels;
	console.log(link);

	request.get(link, function (error, response, body) {
		if (!error && response.statusCode === 200) {
			console.log(body);
		} else {
			console.log(response.statusCode);
			console.log(error);
		}
	});
});
