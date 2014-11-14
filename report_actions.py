from flask import Flask
from flask import jsonify
from flask import request

import model

app = Flask(__name__)
app.config['DEBUG'] = True


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@app.route('/report/view/<username>')
def view_report(username):
  users = model.User.get_by_id(username)
  test_results = model.TestResult.query(ancestor=users.key).fetch()
  # exclude user from to_dict because it's a Key object and can't be serialized
  answers = [answer.to_dict(exclude=['user', 'csrf_token'])
      for answer in test_results[0].answers]
  print "answers=%s" % answers
  return jsonify({'answers': answers})


@app.route('/report/get_summary')
def get_summary():
  pass


@app.route('/report/list_users')
def list_users():
  users = model.User.query().order(
      model.User.time_created).fetch(projection=[model.User.name])
  usernames = [str(user.name) for user in users]
  return jsonify({'usernames': usernames})
