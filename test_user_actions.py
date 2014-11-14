import json

import base_test
import model
import user_actions

class LoginTest(base_test.FlaskBaseTest):
  def setUp(self):
    base_test.FlaskBaseTest.setUp(self, user_actions)

  def testLogin(self):
    data = json.dumps({'username': 'foo-1'})
    response = self.app.post('/user/login', data=data, content_type='application/json')
    self.assertEquals(200, response.status_code)
    result = json.loads(response.data)
    self.assertIsNone(result['error'])
    self.assertTrue(result['csrf_token'])

    # Attempt to read data back
    user = model.User.get_by_id('foo-1')
    self.assertTrue(user.csrf_token.IsValid(result['csrf_token']))

  def testBogusUsername(self):
    data = json.dumps({'username': 'invalid-user-name'})
    response = self.app.post('/user/login', data=data, content_type='application/json')
    self.assertEquals(400, response.status_code)
    result = json.loads(response.data)
    self.assertTrue(result['error'])
