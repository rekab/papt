#
# Backend model code for generating reports.
#
import jinja2

import model

env = jinja2.Environment(loader=jinja2.PackageLoader(__name__, 'templates'))

# Gmail forbids CSS classes, so we must provide style on every element.
STYLE = {
  'summarytable': 'border-collapse:collapse;border-spacing:0px;'
      'font-family:helvetica,sans-serif',
  'resulttable': 'border-collapse:collapse;border-spacing:0px;'
  'font-family:helvetica,sans-serif;float:right; margin: 10px'
}


def GetUserReport(user, result):
  """Returns an HTML report string based on a model.TestResult."""
  template = env.get_template('report.html')
  return template.render(user=user, result=result, style=STYLE)
