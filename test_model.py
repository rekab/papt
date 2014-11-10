import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed

import model

class BaseTest(unittest.TestCase):
  def setUp(self):
    # First, create an instance of the Testbed class.
    self.testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
    self.testbed.activate()
    # Next, declare which service stubs you want to use.
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()

  def tearDown(self):
    self.testbed.deactivate()


class UserTestCase(BaseTest):
  def testUserWithInvalidGroup(self):
    self.assertRaises(ValueError, model.UserName, 'foo')
    self.assertRaises(ValueError, model.UserName, 'foo-12')
    self.assertRaises(ValueError, model.UserName, 'foo-9')
    self.assertRaises(ValueError, model.UserName, 'foo-0')
    model.User(name=model.UserName('foo-1'))
    model.User(name=model.UserName('foo-2'))

  def testUserWithWrongType(self):
    self.assertRaises(TypeError, model.User, name='foo')

  def testUser(self):
    user = model.User(name=model.UserName('foo-1'),
        csrf_token=model.UserCSRFToken(token='asdf'))
    key = user.put()
    fetched = model.User.query(
        model.User.name == model.UserName('foo-1')).fetch()
    self.assertEqual(1, len(fetched))
    self.assertEqual('1', fetched[0].group)
    self.assertTrue(user.csrf_token.IsValid('asdf'))
    self.assertFalse(user.csrf_token.IsValid('nope'))


class TestResultTestCase(BaseTest):

  def testGroup1Answers(self):
    user1 = model.User(name=model.UserName('user-1'))
    user1.put()

    answer = model.TestAnswer(user=user1.key, expected='pair', got='pair')
    result = model.TestResult(parent=user1.key, answers=[answer])
    result.put()
    # Expect that "pair" for a user in group 1 to be categorized as "dm-imm".
    # See static/data/word-categories.json.
    self.assertEqual('dm-imm', result.answers[0].category)
    self.assertTrue(result.answers[0].correct)

    answer = model.TestAnswer(user=user1.key, expected='save', got='recover')
    result.answers.append(answer)
    result.put()

    readback = result.key.get()
    self.assertEqual('dm-imm', readback.answers[0].category)
    self.assertTrue(readback.answers[0].correct)
    self.assertEqual('nt-imm', readback.answers[1].category)
    self.assertFalse(readback.answers[1].correct)


if __name__ == '__main__':
  unittest.main()
