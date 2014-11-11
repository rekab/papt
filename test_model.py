import json
import os

import base_test
import model


def GetExpectedAnswersForTest(flavor):
  path = os.path.join(
      os.path.split(__file__)[0], 'static/data/wordpairs-%s.json' % flavor)
  with open(path) as f:
    return [pair[1] for pair in json.loads(f.read())]


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

  def testCategorization(self):
    user1_key = model.User(name=model.UserName('user-1')).put()
    user2_key = model.User(name=model.UserName('user-2')).put()

    word_categories = model.GetWordCategoriesJsonData()
    def MakeCompletedResults(userkey):
      all_answers = [model.TestAnswer(user=userkey, expected=word, got='grapes')
          for word in word_categories.keys()]
      result = model.TestResult(parent=userkey, answers=all_answers)
      self.assertTrue(result.AllWordsAnswered())
      return result

    user1_results = MakeCompletedResults(user1_key)
    user2_results = MakeCompletedResults(user2_key)

    wordpair_answers = {
        flavor: GetExpectedAnswersForTest(flavor) for flavor in ['a', 'b', 'c', 'd']
        }

    def VerifyCategoryForTestFlavor(flavor, test1_category, test2_category, results):
      # Get all the answers the user was tested on.
      answers_to_category = {
          answer.expected: answer.category for answer in results.answers
          }
      # Intersect that list with the wordpair data of a particular flavor.
      words_tested = set(wordpair_answers[flavor]).intersection(
          answers_to_category.keys())

      # Verify the intersection isn't empty.
      self.assertTrue(words_tested)

      # Verify each word from that wordpair flavor has the expected category.
      for word in words_tested:
        if word_categories[word][2] == 'test-1':
          expected_category = test1_category
        else:
          expected_category = test2_category

        self.assertEqual(expected_category, answers_to_category[word], 
            'word=%s expected_category=%s got=%s' % (
              word, expected_category, answers_to_category[word]))

    # Verify that, for a user in group 1, the words from 'wordpairs-a.json'
    # that appear in test-1 are categorized as 'dm-imm', and words that appear
    # in test-2 are 'dm-del'.
    VerifyCategoryForTestFlavor('a', 'dm-imm', 'dm-del', user1_results)

    # Verify that, for a user in group 2, the words from 'wordpairs-a.json'
    # that appear in test-1 are categorized as 'nt-del', and words that appear
    # in test-2 are 'nt-imm'.
    VerifyCategoryForTestFlavor('a', 'nt-del', 'nt-imm', user2_results)

    VerifyCategoryForTestFlavor('b', 'nt-imm', 'nt-del', user1_results)
    VerifyCategoryForTestFlavor('b', 'dm-del', 'dm-imm', user2_results)

    VerifyCategoryForTestFlavor('c', 'dm-imm', 'dm-del', user1_results)
    VerifyCategoryForTestFlavor('c', 'nt-del', 'nt-imm', user2_results)
    
    VerifyCategoryForTestFlavor('d', 'nt-imm', 'nt-del', user1_results)
    VerifyCategoryForTestFlavor('d', 'dm-del', 'dm-imm', user2_results)


if __name__ == '__main__':
  unittest.main()
