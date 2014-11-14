#
# Backend model code for generating reports.
#
import jinja2

import model

env = jinja2.Environment(loader=jinja2.PackageLoader(__name__, 'templates'))

class Totals(object):
  # TODO: these should be computed properties of the testresult
  def __init__(self, result):
    self.nt_imm = sum(answer.correct for answer in result.answers if answer.category=='nt-imm')
    self.dm_imm = sum(answer.correct for answer in result.answers if answer.category=='dm-imm')
    self.nt_del = sum(answer.correct for answer in result.answers if answer.category=='nt-del')
    self.dm_del = sum(answer.correct for answer in result.answers if answer.category=='dm-del')


def GetReport(user, result):
  """Returns an HTML report string based on a model.TestResult."""
  template = env.get_template('report.html')
  totals = Totals(result)
  return template.render(user=user, totals=totals, result=result)
