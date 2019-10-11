# Header something something something

from mongoengine import *

# db.myCollection.insert({"name": "john", "age" : 22, "location": "colombo"})


class Question(Document):
  questionText = StringField(required = True, max_length = 50)
  #yesSeverity =
  #noSeverity =
  #otherSeverity =
  #otherText =


class AuditTemplate(Document):
  title = StringField(required = True, max_length = 50)
  questions = ListField(ReferenceField(Question), required = True)


class AuditTemplateBuilder:
