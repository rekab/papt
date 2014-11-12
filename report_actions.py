from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)
app.config['DEBUG'] = True


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@app.route('/report/view/<username>')
def view_report(username):
  return reports.GetReport(username)


@app.route('/report/summary')
def get_summary():
  pass

@app.route('/report/list')
def list_reports():
  pass
