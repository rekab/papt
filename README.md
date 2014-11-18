## PAPT

Baker Paired Association Program (B-PAP).

The B-PAP is a word pair presentation and testing computer program, based on
Google App Engine using [AngularJS](http://angularjs.org/) and the 
[Flask micro framework](http://flask.pocoo.org).

## Project Goals

1. The B-PAP will be given an obscure URL that cannot be found during a web search.  

2. The first screen will require the experimenter to enter the participant code.

3. After entering the code, the experimenter will click either the "Initial
Learning Phase [A, B, C, or D]," "Test 1," or "Test 2" buttons.  

4. The Initial Learning Phases will present participants with the four sets of
11 word pairs.  Each word pair will be presented at 1-minute intervals to allow
adequate time to create an image.  A 500-millisecond lapse will occur between
each word pair similar to the study by Coane (2013).  Word pairs will be
displayed in 72-point Helvetica font, and the first word will have a colon
after it (e.g., SWEET : FISH).  A display bar will indicate how much time is
remaining for each item, and a tone will sound after one minute has passed,
alerting participants to the next question.  

5. Test 1 will test participants on 22 word pairs (11 word pairs from the DM
condition and 11 from the NT condition) by displaying a word and an adjacent
text box where participants will type the associated word.  Test 2 will test
participants on the remaining word pairs. 

### Scoring

See [scoring_model.md](scoring_model.md).

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

