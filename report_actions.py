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
  test_results = model.TestResult.query(ancestor=user.key).fetch()
  # exclude user from to_dict because it's a Key object and can't be serialized
  answers = [answer.to_dict(exclude=['user'])
      for answer in test_results[0].answers]
  print "user=%s answers=%s" % (user, answers)
  return report_generator.GetReport(user, test_results[0])


@app.route('/report/get_summary')
def get_summary():
  pass


@app.route('/report/list_users')
def list_users():
  users = model.User.query().order(
      model.User.time_created).fetch(projection=[model.User.name])
  usernames = [str(user.name) for user in users]
  return jsonify({'usernames': usernames})
