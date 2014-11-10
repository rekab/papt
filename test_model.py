import base_test
import model

class UserTestCase(base_test.BaseTest):
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


class TestResultTestCase(base_test.BaseTest):

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

  def testAnswersAreComplete(self):
    user1 = model.User(name=model.UserName('user-1'))

    # Test a result with only one answer.
    result = model.TestResult(
        parent=user1.key,
        answers=[model.TestAnswer(user=user1.key, expected='pair', got='pair')])
    self.assertFalse(result.AllWordsAnswered())

    # Add all the answers.
    for word in model.WordCategorizer.GetTestWords():
      result.answers.append(model.TestAnswer(user=user1.key, expected=word))

    # Verify all words accounted for.
    self.assertTrue(result.AllWordsAnswered())


if __name__ == '__main__':
  unittest.main()
