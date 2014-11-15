#
# Backend model code for generating reports.
#
import jinja2

import model

env = jinja2.Environment(loader=jinja2.PackageLoader(__name__, 'templates'))

# CSS in gmail does not use classes, so we must express style on every element.
STYLE = {
  'table': "border-collapse:collapse;border-spacing:0px;font-family:helvetica,sans-serif;"
}


def GetReport(user, result):
  """Returns an HTML report string based on a model.TestResult."""
  template = env.get_template('report.html')
  return template.render(user=user, result=result, style=STYLE)
