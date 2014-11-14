import json

import base_test
import model
import report_actions


class TestReportActions(base_test.FlaskBaseTest):
  def setUp(self):
    base_test.FlaskBaseTest.setUp(self, report_actions)

  def testListUsers(self):
    for username in ['foo-1', 'bar-2']:
      model.User(id=username, name=model.UserName(username)).put()
    response = self.app.get('/report/list_users')
    self.assertEquals(200, response.status_code)
    data = json.loads(response.data)
    self.assertEquals(len(data['usernames']), 2)
    self.assertEquals(data['usernames'][0], 'foo-1')
    self.assertEquals(data['usernames'][1], 'bar-2')
