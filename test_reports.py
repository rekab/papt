import base_test
import model
import reports


class TestTest(base_test.BaseTest):
  def setUp(self):
    base_test.BaseTest.setUp(self)

  def testSendReport(self):
    username = 'user-report-1'
    base_test.CreateUserWithToken(username, 'csrftoken')
