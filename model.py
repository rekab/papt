"""Models of results for storage in NDB."""
import json
import os
import re

from google.appengine.ext import ndb

USER_NAME_RE = re.compile(r'^[\w\d\-]+-(\d+)$')


class WordCategorizer(object):
  _categories = None

  @staticmethod
  def CategorizeWord(word, group):
    group_num = int(group) - 1
    if group_num not in (0, 1):
      raise ValueError("Invalid group number: %s" % group)

    if not WordCategorizer._categories:
      path = os.path.join(os.path.split(__file__)[0], 'static/data/word-categories.json')
      with open(path) as f:
        WordCategorizer._categories = json.loads(f.read())

    return WordCategorizer._categories[word][group_num]


class UserName(object):
  """Validation/convenience class to store user names.

  User names should be "<string>-<group number>".
  """

  def __init__(self, name):
    """Constructor.
    
    Args:
      name: string, assumed to have been validated.
    """
    self.name = name
    m = USER_NAME_RE.match(name)
    if not m:
      raise ValueError('Invalid user name: %s' % name)
    self.group = m.group(1)


class UserNameProperty(ndb.StringProperty):

  def _validate(self, value):
    if not isinstance(value, UserName):
      raise TypeError('%s is not a UserName object' % value)

  def _to_base_type(self, value):
    """Store the value for the datastore."""
    return value.name

  def _from_base_type(self, value):
    return UserName(value)


class User(ndb.Model):
  """A user and their results."""
  name = UserNameProperty()
  group = ndb.ComputedProperty(lambda self: self.name.group)
  time_created = ndb.DateTimeProperty(auto_now_add=True)
  notetaking_time = ndb.DateTimeProperty()
  drawing_time = ndb.DateTimeProperty()

#class WordCategory(object):
#  """Validation/convenience class to store word category.
#  
#  Each test answer belongs to a category based on the user's login id.
#  """
#  def __init__(self, word, group):
#
#
#class WordCategoryProperty(ndb.StringProperty):
#  def _validate(self, value):
#    if not isinstance(value, WordCategory):
#      raise TypeError("%s is not a WordCategory object" % value)
#
#  def _to_base_type(self, value):
#    pass
#
#  def _from_base_type(self, value):

class TestAnswer(ndb.Model):
  user = ndb.KeyProperty(kind=User)
  time_answered = ndb.DateTimeProperty(auto_now_add=True)
  expected = ndb.StringProperty()
  got = ndb.StringProperty()
  correct = ndb.BooleanProperty()
  category = ndb.ComputedProperty(
      # Lookup the category of the word based on the user's group.
      lambda self: WordCategorizer.CategorizeWord(
        self.expected, self.user.get().group))


class TestResult(ndb.Model):
  time_taken = ndb.DateTimeProperty(auto_now_add=True)
  answers = ndb.StructuredProperty(TestAnswer, repeated=True)
