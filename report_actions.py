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
  # Get all the test results and return them as json. Offload all the
  # processing to the client.
  response_data = []
  results = model.TestResult.query().fetch()
  for result in results:
    for answer in result.answers:
      # exclude "user": it's a Key object that can't be serialized
      response_data.append(answer.to_dict(exclude=['user']))
  return jsonify({'answers': response_data})


def JsonifyDrilldownData(results, comparator):
  response_data = []
  for result in results:
    for answer in result.answers:
      if comparator(answer):
        # Exclude "user": it's a Key object that can't be serialized.
        datum = answer.to_dict(exclude=['user'])
        # Convert it to a string instead.
        datum['username'] = str(answer.user.get().name)
        response_data.append(datum)
  return jsonify({'answers': response_data})


@app.route('/report/drilldown/word/<word>')
def get_drilldown_word(word):
  return JsonifyDrilldownData(model.TestResult.query(
      model.TestResult.answers.expected==word).fetch(),
      lambda answer: answer.expected == word)


@app.route('/report/drilldown/category/<category>')
def get_drilldown_category(category):
  return JsonifyDrilldownData(model.TestResult.query(
      model.TestResult.answers.category==category).fetch(),
      lambda answer: answer.category == category)


@app.route('/report/list_users')
def list_users():
  users = model.User.query().order(
      model.User.time_created).fetch(projection=[model.User.name])
  usernames = [str(user.name) for user in users]
  return jsonify({'usernames': usernames})
