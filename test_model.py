import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed

import results

class UserTestCase(unittest.TestCase):
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

  def testUserWithInvalidGroup(self):
    self.assertRaises(TypeError, results.User, name='foo')

  def testUser(self):
    user = results.User(name=results.UserName('foo-1'))
    key = user.put()
    fetched = results.User.query(
        results.User.name == results.UserName('foo-1')).fetch()
    self.assertEqual(1, len(fetched))
    self.assertEqual('1', fetched[0].group)


if __name__ == '__main__':
  unittest.main()
