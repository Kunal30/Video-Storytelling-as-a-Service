// The Cloud Functions for Firebase SDK to create Cloud Functions and setup triggers.
const functions = require('firebase-functions');

// The Firebase Admin SDK to access the Firebase Realtime Database.
const admin = require('firebase-admin');
admin.initializeApp();

// Imports the Google Cloud Video Intelligence library
const videoIntelligence = require('@google-cloud/video-intelligence');


exports.annotateVideos = functions.storage.object().onFinalize(async (object) => {

	// Creates a client
	const client = new videoIntelligence.VideoIntelligenceServiceClient();

	// The GCS uri of the video to analyze
	const gcsUri = 'gs://video-storytelling-37f0c.appspot.com/' + object.name;

	// Construct request
	const request = {
	  inputUri: gcsUri,
	  features: ['LABEL_DETECTION'],
	};

	// Execute request
	const [operation] = await client.annotateVideo(request);

	console.log(
	  'Waiting for operation to complete... (this may take a few minutes)'
	);

	const [operationResult] = await operation.promise();

	// Gets annotations for video
	const annotations = operationResult.annotationResults[0];

	// Gets labels for video from its annotations
	const labels = annotations.segmentLabelAnnotations;
	labels.forEach(label => {
	  console.log(`Label ${label.entity.description} occurs at:`);
	  label.segments.forEach(segment => {
	    segment = segment.segment;
	    if (segment.startTimeOffset.seconds === undefined) {
	      segment.startTimeOffset.seconds = 0;
	    }
	    if (segment.startTimeOffset.nanos === undefined) {
	      segment.startTimeOffset.nanos = 0;
	    }
	    if (segment.endTimeOffset.seconds === undefined) {
	      segment.endTimeOffset.seconds = 0;
	    }
	    if (segment.endTimeOffset.nanos === undefined) {
	      segment.endTimeOffset.nanos = 0;
	    }
	    console.log(
	      `\tStart: ${segment.startTimeOffset.seconds}` +
	        `.${(segment.startTimeOffset.nanos / 1e6).toFixed(0)}s`
	    );
	    console.log(
	      `\tEnd: ${segment.endTimeOffset.seconds}.` +
	        `${(segment.endTimeOffset.nanos / 1e6).toFixed(0)}s`
	    );
	  });
	});
});
