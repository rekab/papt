import logging

from flask import Flask
from flask import jsonify
from flask import request

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
  user, posted_json = validate_json()
  test_results = model.TestResult.query(ancestor=user.key).fetch()
  if test_results:
    test_result = test_results[0]
  else:
    test_result = model.TestResult(parent=user.key)
  start = model.TestStart(test_flavor=posted_json['test_flavor'])
  test_result.tests_started.append(start)
  test_result.put()
  return jsonify(message='ok')


def GetTestResult(user_key):
  test_results = model.TestResult.query(ancestor=user_key).fetch()
  for test_result in test_results:
    return test_result
  raise NoTestInProgress()


@app.route('/test/finish', methods=['POST'])
def finish():
  user, posted_json = validate_json()

  test_results = model.TestResult.query(ancestor=user.key).fetch()
  if not test_results:
    error = 'No test currently in progress'
    logging.error(error)
    response = jsonify({'error': error})
    response.status_code = 400
    return response
  test_result = test_results[0]
  finish = model.TestFinish(test_flavor=posted_json['test_flavor'])
  test_result.tests_finished.append(finish)
  test_result.put()
  return jsonify(message='ok')


@app.route('/test/answer', methods=['POST'])
def answer():
  user, posted_json = validate_json()
  if 'expected' not in posted_json:
    raise BadJsonPost('no expected word provided')
  if 'answer' not in posted_json:
    raise BadJsonPost('no answer provided')

  test_results = model.TestResult.query(ancestor=user.key).fetch()
  if not test_results:
    raise NoTestInProgress()
  test_result = test_results[0]

  answer = model.TestAnswer(
      user=user.key,
      expected=posted_json['expected'], 
      got=posted_json['answer'],
      test_flavor=posted_json['test_flavor'])
  logging.info('Saving answer %(answer)s (flavor=%(test_flavor)s)', posted_json)

  test_result.answers.append(answer)
  test_result.put()
  return jsonify(message='ok', done=test_result.AllWordsAnswered())


def validate_json():
  posted_json = request.get_json()
  if not posted_json:
    raise BadJsonPost('no json sent')

  for key in REQUIRED_ANSWER_JSON_KEYS:
    if key not in posted_json:
      raise BadJsonPost('bad json post: %s not present in %s' % (key, posted_json))

  user = model.User.get_by_id(posted_json['username'])
  if not user:
    raise BadJsonPost('unknown user %s' % posted_json['username'])
  if user.csrf_token.token != posted_json['csrf_token']:
    # TODO: check the csrf token generation date
    raise BadJsonPost('bad csrf token for user %s' % posted_json['username'])
  return user, posted_json
