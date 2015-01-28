import datetime
import logging
import mail_settings
import xlsxwriter
import StringIO

from flask import Flask
from flask import jsonify
from flask import request

from google.appengine.api import mail
from google.appengine.ext import ndb

import model

app = Flask(__name__)
app.config['DEBUG'] = True

REQUIRED_ANSWER_JSON_KEYS = ['username', 'csrf_token', 'test_flavor']


class Badness(Exception):
  def __init__(self, message):
    logging.error('raising error: %s', message)
    self.message = message


class BadJsonPost(Badness):
  pass


class NoTestInProgress(Badness):
  def __init__(self):
    Badness.__init__(self, 'No test currently in progress')


@app.errorhandler(Badness)
def handle_invalid_data(error):
  response = jsonify({'error': error.message})
  response.status_code = 400
  return response


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@app.route('/test/start', methods=['POST'])
def start():
  user, posted_json = validate_json(['test_flavor'])
  flavor = posted_json['test_flavor']
  key = ndb.Key(model.TestResult, flavor, parent=user.key)
  test_result = key.get()
  if not test_result:
    model.TestResult(id=flavor, parent=user.key, flavor=flavor).put()
  else:
    # TODO: should this be an error? Support resuming a test?
    logging.error('Started a test that already existed? %d', posted_json)
  return jsonify(message='ok')


def GetTestResult(user_key):
  test_results = model.TestResult.query(ancestor=user_key).fetch()
  for test_result in test_results:
    return test_result
  raise NoTestInProgress()


@app.route('/test/finish', methods=['POST'])
def finish():
  user, posted_json = validate_json(['test_flavor'])
  flavor = posted_json['test_flavor']
  key = ndb.Key(model.TestResult, flavor, parent=user.key)
  test_result = key.get()

  if not test_result:
    error = 'No test currently in progress'
    logging.error(error)
    response = jsonify({'error': error})
    response.status_code = 400
    return response

  test_result.time_finished = datetime.datetime.now()
  test_result.put()
  MailTestResult(test_result)
  return jsonify(message='ok')


def MailTestResult(test_result):
  src = mail_settings.EMAIL_SOURCE
  dest = mail_settings.EMAIL_DESTINATION
  subject = mail_settings.SUBJECT
  attachment = GenerateExcelFile(test_result)
  mail.send_mail(
      sender=src, to=dest, subject=subject, body="Here's some stuff.",
      attachments=[('papt.xls', attachment)])


def GenerateExcelFile(test_result):
  return 'asdf'


@app.route('/test/answer', methods=['POST'])
def answer():
  user, posted_json = validate_json(['expected', 'answer', 'test_flavor'])
  flavor = posted_json['test_flavor']

  key = ndb.Key(model.TestResult, flavor, parent=user.key)
  test_result = key.get()
  if not test_result:
    raise NoTestInProgress()

  answer = model.TestAnswer(
      user=user.key,
      expected=posted_json['expected'], 
      got=posted_json['answer'],
      test_flavor=flavor)
  logging.info('Saving answer %(answer)s (flavor=%(test_flavor)s)', posted_json)

  test_result.answers.append(answer)
  test_result.put()
  return jsonify(message='ok', done=test_result.AllWordsAnswered())


def validate_json(extra_required_keys=None):
  posted_json = request.get_json()
  if not posted_json:
    raise BadJsonPost('no json sent')

  for key in REQUIRED_ANSWER_JSON_KEYS + (extra_required_keys or []):
    if key not in posted_json:
      raise BadJsonPost('bad json post: "%s" not present in %s' % (key, posted_json))

  user = model.User.get_by_id(posted_json['username'])
  if not user:
    raise BadJsonPost('unknown user %s' % posted_json['username'])
  if user.csrf_token.token != posted_json['csrf_token']:
    # TODO: check the csrf token generation date
    raise BadJsonPost('bad csrf token for user %s' % posted_json['username'])
  return user, posted_json
