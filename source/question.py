from mongoengine import EmbeddedDocument, EmbeddedDocumentField, StringField
from source.severity import Severity


class Question(EmbeddedDocument):
    text  = StringField(required=True, max_length=50, min_length=1)
    yes   = EmbeddedDocumentField(Severity, required=True, default=Severity.default())
    no    = EmbeddedDocumentField(Severity, required=True, default=Severity.default())
    other = EmbeddedDocumentField(Severity, required=True, default=Severity.default())

