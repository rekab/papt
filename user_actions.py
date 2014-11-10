import datetime
import json
import logging
import random
import string
from flask import Flask
from flask import jsonify

import model

app = Flask(__name__)
app.config['DEBUG'] = True

CSRF_TOKEN_LENGTH = 20

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@app.route('/user/login/<username>')
def login(username):
  user = None
  try:
    user = model.User.get_by_id(username)
    if user:
      logging.info('Logging in existing user %s', user)
    else:
      user = model.User(id=username, name=model.UserName(username))
      user.put()
      logging.info('Created user %s', user)
  except (ValueError, TypeError) as e:
    error = jsonify(error=str(e))
    error.status_code = 400
    return error

  # Regenerate the CSRF token.
  token = ''.join(random.choice(string.ascii_lowercase)
      for _ in range(CSRF_TOKEN_LENGTH))
  user.csrf_token = model.UserCSRFToken(
      time_created=datetime.datetime.now(),
      token=token)
  user.put()

  return jsonify(error=None, csrf_token=user.csrf_token.token)


@app.route('/user/logout')
def logout():
  return 'OK'
