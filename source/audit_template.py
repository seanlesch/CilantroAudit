# Header something something something
from mongoengine import Document, StringField, EmbeddedDocumentListField
from question import Question

class AuditTemplate(Document):
    title = StringField(required=True, max_length=50, min_length=1)
    questions = EmbeddedDocumentListField(Question, required=True)
