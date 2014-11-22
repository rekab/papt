import json

import base_test
import model
import report_actions

from google.appengine.ext import ndb


class TestReportActions(base_test.FlaskBaseTest):
  def setUp(self):
    base_test.FlaskBaseTest.setUp(self, report_actions)

  def PutUser(self, username):
    return model.User(id=username, name=model.UserName(username)).put()

  def testListUsers(self):
    for username in ['foo-1', 'bar-2']:
      self.PutUser(username)
    response = self.app.get('/report/list_users')
    self.assertEquals(200, response.status_code)
    data = json.loads(response.data)
    self.assertEquals(len(data['usernames']), 2)
    self.assertEquals(data['usernames'][0], 'foo-1')
    self.assertEquals(data['usernames'][1], 'bar-2')

  def testViewReportMissingUser(self):
    self.VerifyUnhappyResponse(self.app.get('/report/view/foo'))

  def testViewReportNoTest(self):
    username = 'foo-1'
    self.PutUser(username)
    self.VerifyUnhappyResponse(self.app.get('/report/view/' + username))

  def PutTestResult(self, user_key, flavor, answers):
    result = model.TestResult(id=flavor, parent=user_key, flavor=flavor)
    for answer in answers:
      result.answers.append(
          model.TestAnswer(
            user=user_key, expected=answer[0], got=answer[1], test_flavor=flavor))
    return result.put()

  def testViewReport(self):
    username = 'foo-1'
    user_key = self.PutUser(username)
    self.PutTestResult(user_key, 'foo', [['pair', 'got']])
    self.PutTestResult(user_key, 'bar', [['decay', 'word']])
    response = self.app.get('/report/view/' + username)
    self.assertEquals(200, response.status_code)
    self.assertTrue('report' in response.data)

  def testGetSummary(self):
    user_key = self.PutUser('foo-1')
    self.PutTestResult(user_key, 'foo', [['pair', 'got']])
    user_key = self.PutUser('bar-2')
    self.PutTestResult(user_key, 'bar', [['decay', 'word']])
    response = self.app.get('/report/get_summary')
    self.assertEquals(200, response.status_code)
    data = json.loads(response.data)
    self.assertEquals(2, len(data['answers']))
    self.assertEquals('decay', data['answers'][0]['expected'])
    self.assertEquals('word', data['answers'][0]['got'])
    self.assertEquals('pair', data['answers'][1]['expected'])
    self.assertEquals('got', data['answers'][1]['got'])

  def testGetDrilldown(self):
    user_key = self.PutUser('foo-1')
    self.PutTestResult(user_key, 'foo', [['pair', 'got'], ['decay', 'fuzz']])
    self.PutTestResult(user_key, 'bar', [['baby', 'stuff']])
    response = self.app.get('/report/drilldown/pair')
    self.assertEquals(200, response.status_code)
    data = json.loads(response.data)
    self.assertEquals(1, len(data['answers']))
    self.assertEquals('pair', data['answers'][0]['expected'])
    self.assertEquals('got', data['answers'][0]['got'])
    self.assertEquals('foo-1', data['answers'][0]['username'])
