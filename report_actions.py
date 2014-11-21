import jinja2

from flask import Flask
from flask import jsonify
from flask import request

import model
import report_generator

app = Flask(__name__)
app.config['DEBUG'] = True


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@app.route('/report/view/<username>')
def view_report(username):
  user = model.User.get_by_id(username)
  if not user:
    error = jsonify({'error': 'User "%s" does not exist' % username})
    error.status_code = 400;
    return error

  test_results = model.TestResult.query(ancestor=user.key).fetch()
  if not test_results:
    error = jsonify({'error': 'User "%s" did not take a test' % username})
    error.status_code = 400;
    return error

  return jsonify({'report':report_generator.GetUserReport(user, test_results)})


@app.route('/report/get_summary')
def get_summary():
  pass


@app.route('/report/list_users')
def list_users():
  users = model.User.query().order(
      model.User.time_created).fetch(projection=[model.User.name])
  usernames = [str(user.name) for user in users]
  return jsonify({'usernames': usernames})
