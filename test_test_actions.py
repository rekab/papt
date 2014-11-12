import json

import base_test
import model
import test_actions


class TestTest(base_test.BaseTest):
  def setUp(self):
    base_test.BaseTest.setUp(self)
    test_actions.app.config['TESTING'] = True
    self.app = test_actions.app.test_client()

  def testMissingUsername(self):
    data = json.dumps({})
    response = self.app.post('/test/answer', data=data, content_type='application/json')
    self.assertEquals(400, response.status_code)
    result = json.loads(response.data)
    self.assertTrue('bad json post' in result['error'])

  def testUnknownUser(self):
    data = json.dumps({'username': 'no-such-user-1', 'csrf_token': 'aaaa'})
    response = self.app.post('/test/answer', data=data, content_type='application/json')
    self.assertEquals(400, response.status_code)
    result = json.loads(response.data)
    self.assertTrue('unknown user' in result['error'])

  def testBadCSRFToken(self):
    username = 'csrf-user-test-1'
    base_test.CreateUserWithToken(username, 'foobar')

    data = json.dumps({'username': username, 'csrf_token': 'this will not match'})
    response = self.app.post('/test/answer', data=data, content_type='application/json')
    self.assertEquals(400, response.status_code)
    result = json.loads(response.data)
    self.assertTrue('bad csrf token' in result['error'])

  def testMissingExpectedWord(self):
    username = 'user-without-an-expected-word-1'
    token = 'foo'
    base_test.CreateUserWithToken(username, token)
    data = json.dumps({'username': username, 'csrf_token': token, 'answer': 'foo'})
    response = self.app.post('/test/answer', data=data, content_type='application/json')
    self.assertEquals(400, response.status_code)
    result = json.loads(response.data)
    self.assertTrue('no expected word provided' in result['error'])

  def testMissingAnswer(self):
    username = 'user-without-an-answer-1'
    token = 'foo'
    base_test.CreateUserWithToken(username, token)
    data = json.dumps({'username': username, 'csrf_token': token, 'expected': 'foo'})
    response = self.app.post('/test/answer', data=data, content_type='application/json')
    self.assertEquals(400, response.status_code)
    result = json.loads(response.data)
    self.assertTrue('no answer provided' in result['error'])

  def testRecordAnswer(self):
    username = 'user-answers-1'
    token = 'foo'
    base_test.CreateUserWithToken(username, token)
    self.PostAnswer(username, token, 'pair')  # this word must come from static/data/word-categories.json

    # Verify the user's result
    user = model.User.get_by_id(username)
    test_results = model.TestResult.query(ancestor=user.key).fetch()
    self.assertEquals(1, len(test_results))
    self.assertEquals(1, len(test_results[0].answers))
    self.assertEquals('pair', test_results[0].answers[0].expected)
    self.assertEquals('pants', test_results[0].answers[0].got)
    self.assertFalse(test_results[0].answers[0].correct)

  def PostAnswer(self, username, token, expected):
    data = json.dumps({
      'username': username,
      'csrf_token': token,
      'answer': 'pants',
      'expected': expected}) 
    response = self.app.post('/test/answer', data=data, content_type='application/json')
    self.assertEquals(200, response.status_code)
    result = json.loads(response.data)
    self.assertEqual('ok', result['message'])
    self.assertFalse(result['done'])

  def testUserFinishesTest(self):
    username = 'user-answers-everything-2'
    token = 'foo'
    base_test.CreateUserWithToken(username, token)
    words = model.WordCategorizer.GetTestWords()
    last_word = words.pop()

    for word in words:
      self.PostAnswer(username, token, word)

    data = json.dumps({
      'username': username,
      'csrf_token': token,
      'answer': 'pants',
      'expected': last_word}) 
    response = self.app.post('/test/answer', data=data, content_type='application/json')
    self.assertEquals(200, response.status_code)
    result = json.loads(response.data)
    self.assertEqual('ok', result['message'])
    # Should be done now!
    self.assertTrue(result['done'])

