import logging

from flask import Flask
from flask import jsonify
from flask import request

import model

app = Flask(__name__)
app.config['DEBUG'] = True

class BadJsonPost(Exception):
  def __init__(self, message):
    logging.error('raising error: %s', message)
    self.message = message


@app.errorhandler(BadJsonPost)
def handle_invalid_data(error):
  response = jsonify({'error': error.message})
  response.status_code = 400
  return response


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@app.route('/test/answer', methods=['POST'])
def answer():
  user, posted_json = validate_json()
  if 'expected' not in posted_json:
    raise BadJsonPost('no expected word provided')
  if 'answer' not in posted_json:
    raise BadJsonPost('no answer provided')
  test_results = model.TestResult.query(ancestor=user.key).fetch()
  for test_result in test_results:
    break
  else:
    test_result = model.TestResult(parent=user.key)

  answer = model.TestAnswer(
      user=user.key,
      expected=posted_json['expected'], 
      got=posted_json['answer'])

  test_result.answers.append(answer)
  test_result.put()
  return jsonify(message='ok', done=test_result.AllWordsAnswered())


def validate_json():
  posted_json = request.get_json()
  if not posted_json or 'username' not in posted_json or 'csrf_token' not in posted_json:
    error = 'bad json post: %s' % posted_json
    raise BadJsonPost(error)
  user = model.User.get_by_id(posted_json['username'])
  if not user:
    raise BadJsonPost('unknown user %s' % posted_json['username'])
  if user.csrf_token.token != posted_json['csrf_token']:
    # TODO: check the csrf token generation date
    raise BadJsonPost('bad csrf token for user %s' % posted_json['username'])
  return user, posted_json