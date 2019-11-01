from datetime import datetime

from mongoengine import Document, StringField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField, \
    EmbeddedDocumentListField, ValidationError

from cilantro_audit.audit_template import Severity
from cilantro_audit.constants import TEXT_MIN_LENGTH, TEXT_MAX_LENGTH, COMMENT_MIN_LENGTH, COMMENT_MAX_LENGTH, \
    TITLE_MAX_LENGTH, TITLE_MIN_LENGTH, AUDITOR_MAX_LENGTH, AUDITOR_MIN_LENGTH


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
    text = StringField(required=True, max_length=TEXT_MAX_LENGTH, min_length=TEXT_MIN_LENGTH)
    severity = EmbeddedDocumentField(Severity, required=True)
    response = EmbeddedDocumentField(Response, required=True)
    comment = StringField(max_length=COMMENT_MAX_LENGTH, min_length=COMMENT_MIN_LENGTH)

    def validate(self, clean=True):
        super().validate(clean)
        if self.response == Response.other() and self.comment is None:
            raise ValidationError("All questions marked OTHER must have a comment.")


class CompletedAuditBuilder:
    def __init__(self):
        self.title = None
        self.datetime = None
        self.auditor = None
        self.max_severity = Severity.green()
        self.answers = []

    def with_title(self, title):
        self.title = title
        return self

    def with_auditor(self, auditor):
        self.auditor = auditor
        return self

    def with_answer(self, answer):
        self.answers.append(answer)
        if answer.severity == Severity.red():
            self.max_severity = Severity.red()
        elif self.max_severity == Severity.green() and answer.severity == Severity.yellow():
            self.max_severity = Severity.yellow()
        return self

    def build(self):
        audit = CompletedAudit(
            title=self.title,
            datetime=datetime.utcnow(),
            auditor=self.auditor,
            severity=self.max_severity,
            answers=self.answers,
        )
        audit.validate()
        return audit


class CompletedAudit(Document):
    title = StringField(required=True, max_length=TITLE_MAX_LENGTH, min_length=TITLE_MIN_LENGTH)
    datetime = DateTimeField(required=True)
    auditor = StringField(required=True, max_length=AUDITOR_MAX_LENGTH, min_length=AUDITOR_MIN_LENGTH)
    severity = EmbeddedDocumentField(Severity, required=True)
    answers = EmbeddedDocumentListField(Answer, required=True)
