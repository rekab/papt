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

class TestResultsSummary(object):
  sum_nt_imm = 0
  sum_dm_imm = 0
  sum_nt_del = 0
  sum_dm_del = 0

  def AddResult(self, result):
    self.sum_nt_imm += result.sum_nt_imm
    self.sum_dm_imm += result.sum_dm_imm
    self.sum_nt_del += result.sum_nt_del
    self.sum_dm_del += result.sum_dm_del


def DatetimeFilter(d):
  #return d.astimezone(tz.gettz('PST8PDT')).strftime('%Y-%m-%d ')
  #return d.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('PST8PDT'))
  return d.strftime('%Y-%m-%d %H:%M:%S UTC')


env.filters['DatetimeFilter'] = DatetimeFilter


def GetUserReport(user, results):
  """Returns an HTML report string based on list of model.TestResults."""
  template = env.get_template('report.html')
  summary = TestResultsSummary()
  for result in results:
    summary.AddResult(result)
  return template.render(user=user, summary=summary, results=results, style=STYLE)
