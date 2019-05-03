## Real-Time Video-Storytelling As A Service

### Requirements
```sh
bash terminal (although Windows / Mac OS can be used too with different commands)
gcloud (and python-app-engine using gcloud)
nvm (install node and npm using nvm)
adb (for installing android app in mobile device)
```
### Installation Steps:
* Create google cloud project, get its PROJECT_ID
	*Enable Video Intelligence API for this project
* Create a firebase project associated with this project
* In Firebase Storage Website
	* Create firebase storage bucket with name STORAGE_NAME, this will contain all the videos recorded by user through the android application
	* Make public in rules
```sh
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read, write;
    }
  }
}
```
* In Firebase Realtime Database Website
	* Create a database in test mode (if creating for the first time)
	* Create two firebase realtime databases with names LABELS_DATABASE_NAME and STORIES_DATABASE_NAME, these two databases will hold labels generated by video-intelligence-labelling-service and stories generated by nltk-story-generation-service respectively
	* Make public in rules
```sh
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```
* In Firebase Project Settings Website
	* Go to service accounts
	* Generate new private key
	* Let the downloaded authorization file be called AUTH_FILE
* In appengine-services directory
	* Copy AUTH_FILE in /video-intelligence-labelling-service directory
	* Copy AUTH_FILE in /nltk-story-generation-service directory
	* In /video-intelligence-labelling-service/main.py, update STORAGE_NAME, LABELS_DATABASE_NAME and AUTH_FILE variables
	* In /nltk-story-generation-service/main.py, update STORIES_DATABASE_NAME and AUTH_FILE variables
	* Deploy these two services as a part of the same app engine project
			gcloud app deploy video-intelligence-labelling-service/app.yaml \
nltk-story-generation-service/app.yaml
	* video-intelligence-labelling-service will generate labels from videos it accesses from the STORAGE_NAME and store it in LABELS_DATABASE_NAME, while nltk-story-generation-service will generate story for these labels amd store it in STORIES_DATABASE_NAME. For the app engine project to interact successfully with firebase project, it needs AUTH_FILE
* In firebase-functions directory
	* In /functions/index.js, update variables PROJECT_NAME, STORAGE_NAME and LABELS_DATABASE_NAME 
	* Use node version 8
	```sh
		nvm use 8
	```
	* Install firebase-tools globally
	```sh
		npm install -g firebase-tools
	```
	* Login to to the firebase
```sh
		firebase login
```
	* Initialize firebase functions (choose N for file override, choose Y for installing npm dependencies)
```sh
		firebase init functions
```
	* Deploy firebase functions
```sh
		firebase deploy --only functions
```
	* These firebase functions, triggered by change in STORAGE_NAME and LABELS_DATABASE_NAME, make a RESTful API call to video-intelligence-labelling-service and nltk-story-generation-service respectively, passing them necessary information through query parameters
* In Firebase Authentication Website
	* Go to Sign-in method
	* Enable Anonymous for Sign-in providers, this is required since we are not asking users for authentication right now
* In Project Overview Website
	* Click on android icon in “Add an app to get started”
	* Enter android package name as “com.cloud.videostorytelling”
	* Click on Register app
	* Click on “Download google-services.json”, this is our config file for android project
	* Click on X icon to quit out of the steps
* In android-app directory
	* Copy “google-services.json” to /app directory
	* In /app/src/main/java/com/cloud/videostorytelling/Camera2VideoFragment.java, update STORAGE_NAME, LABELS_DATABASE_NAME and STORIES_DATABASE_NAME.
	* Run the following bash command
	bash gradlew clean build
	* Connect Android OS based mobile device to the system through USB cable and run the following bash command
```sh
		adb install ./app/build/outputs/apk/debug/app-debug.apk
```


### Contributors and Team Members: 
1. Jay Shah
2. Aditya Govardhan
3. Kunal Suthar