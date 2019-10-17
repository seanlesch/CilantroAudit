from mongoengine import Document, StringField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField, \
    EmbeddedDocumentListField, ValidationError
from audit_template import Severity
from datetime import datetime


class ResponseEnum:
    YES = "YES"
    NO = "NO"
    OTHER = "OTHER"


class Response(EmbeddedDocument):
    response = StringField(required=True)

    @staticmethod
    def yes():
        return Response(ResponseEnum.YES)

    @staticmethod
    def no():
        return Response(ResponseEnum.NO)

    @staticmethod
    def other():
        return Response(ResponseEnum.OTHER)


class Answer(EmbeddedDocument):
    text = StringField(required=True, max_length=50, min_length=1)
    severity = EmbeddedDocumentField(Severity, required=True)
    response = EmbeddedDocumentField(Response, required=True)
    comment = StringField(max_length=150, min_length=1)

    def validate(self, clean=True):
        super().validate(clean)
        if self.response == Response.other() and self.comment is None:
            raise ValidationError("All questions marked OTHER must have a comment.")


class CompletedAuditBuilder:
    def __init__(self):
        self.title = None
        self.datetime = None
        self.auditor = None
        self.answers = []

    def with_title(self, title):
        self.title = title
        return self

    def with_auditor(self, auditor):
        self.auditor = auditor
        return self

    def with_answer(self, answer):
        self.answers.append(answer)
        return self

    def build(self):
        audit = CompletedAudit(
            title=self.title,
            datetime=datetime.utcnow(),
            auditor=self.auditor,
            answers=self.answers,
        )
        audit.validate()
        return audit


class CompletedAudit(Document):
    title = StringField(required=True, max_length=50, min_length=1)
    datetime = DateTimeField(required=True)
    auditor = StringField(required=True, max_length=50, min_length=1)
    answers = EmbeddedDocumentListField(Answer, required=True)
