import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed

import model


def CreateUserWithToken(username, token):
  user = model.User(id=username, name=model.UserName(username))
  user.csrf_token = model.UserCSRFToken(token=token)
  user.put()


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


class FlaskBaseTest(BaseTest):
  def setUp(self, module_under_test):
    BaseTest.setUp(self)
    # Setup test flask context
    module_under_test.app.config['TESTING'] = True
    self.app = module_under_test.app.test_client()
