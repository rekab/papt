"""Models of results for storage in NDB."""
import re
from google.appengine.ext import ndb

USER_NAME_RE = re.compile(r'^[\w\d\-]+-(\d+)$')

class TestAnswer(ndb.Model):
  time_answered = ndb.DateTimeProperty(auto_now_add=True)
  expected = ndb.StringProperty()
  got = ndb.StringProperty()
  correct = ndb.BooleanProperty()


class TestResult(ndb.Model):
  time_taken = ndb.DateTimeProperty(auto_now_add=True)
  answers = ndb.LocalStructuredProperty(TestAnswer, repeated=True)


class UserName(object):
  def __init__(self, name):
    """Constructor.
    
    Args:
      name: string, assumed to have been validated.
    """
    self.name = name
    m = USER_NAME_RE.match(name)
    if not m:
      raise IllegalArgumentException('Invalid user name: %s' % name)
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
  test1_results = ndb.LocalStructuredProperty(TestResult, repeated=True)
  test2_results = ndb.LocalStructuredProperty(TestResult, repeated=True)
