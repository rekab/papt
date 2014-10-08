## PAPT

Paired Association Presentation and Testing

A Google App Engine app based on [AngularJS](http://angularjs.org/) and the
[Flask micro framework](http://flask.pocoo.org).


## Run Locally
1. Install the [App Engine Python SDK](https://developers.google.com/appengine/downloads).
See the README file for directions. You'll need python 2.7 and [pip 1.4 or later](http://www.pip-installer.org/en/latest/installing.html) installed too.

2. Install node.js and npm.
   ```
   sudo add-apt-repository ppa:chris-lea/node.js
   sudo apt-get update
   sudo apt-get install nodejs
   ```

3. Clone this git repo.

4. Install dependencies in the project's pylib directory.
   Note: App Engine can only import libraries from inside your project directory.

   ```
   cd papt
   pip install -r requirements.txt -t pylib
   ```
5. Run this project locally from the command line:

   ```
   npm start
   ```
   If you run into problems with bower packages, see https://github.com/bower/bower/pull/1403.
   You may also need to run ```npm config set registry http://registry.npmjs.org/```.


Visit the application [http://localhost:8080](http://localhost:8080)

See [the development server documentation](https://developers.google.com/appengine/docs/python/tools/devserver)
for options when running dev_appserver.

## Deploy
To deploy the application:

1. Use the [Admin Console](https://appengine.google.com) to create a
   project/app id. (App id and project id are identical)
1. [Deploy the
   application](https://developers.google.com/appengine/docs/python/tools/uploadinganapp) with

   ```
   appcfg.py -A <your-project-id> --oauth2 update .
   ```
1. Congratulations!  Your application is now live at your-app-id.appspot.com

