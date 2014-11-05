"""Models of results for storage in NDB."""
from google.appengine.ext import ndb


class TestAnswer(ndb.Model):
  time_answered = ndb.DateTimeProperty(auto_now_add=True)
  expected = ndb.StringProperty()
  got = ndb.StringProperty()
  correct = ndb.BooleanProperty()


class TestResult(ndb.Model):
  time_taken = ndb.DateTimeProperty(auto_now_add=True)
  answers = ndb.LocalStructuredProperty(TestAnswer, repeated=True)


class User(ndb.Model):
  """A user and their results."""
  name = ndb.StringProperty()
  time_created = ndb.DateTimeProperty(auto_now_add=True)
  notetaking_time = ndb.DateTimeProperty()
  drawing_time = ndb.DateTimeProperty()
  test1_results = ndb.LocalStructuredProperty(TestResult, repeated=True)
  test2_results = ndb.LocalStructuredProperty(TestResult, repeated=True)
