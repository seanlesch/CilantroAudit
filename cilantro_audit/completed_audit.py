from mongoengine import Document, StringField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField, \
    EmbeddedDocumentListField, ValidationError, BooleanField, IntField

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
    resolved = BooleanField(required=True, default=True)

    def validate(self, clean=True):
        super().validate(clean)
        if self.response == Response.other() and self.comment is None:
            raise ValidationError("All questions marked OTHER must have a comment.")


class CompletedAuditBuilder:
    def __init__(self):
        self.title = None
        self.auditor = None
        self.datetime = None
        self.max_severity = Severity.green()
        self.answers = []
        self.unresolved_count = 0

    def with_title(self, title):
        self.title = title
        return self

    def with_auditor(self, auditor):
        self.auditor = auditor
        return self

    def with_datetime(self, datetime):
        self.datetime = datetime
        return self

    def with_answer(self, answer):
        if answer.severity == Severity.red():
            self.max_severity = Severity.red()
            answer.resolved = False
            self.unresolved_count += 1
        elif self.max_severity == Severity.green() and answer.severity == Severity.yellow():
            self.max_severity = Severity.yellow()
        self.answers.append(answer)
        return self

    def build(self):
        audit = CompletedAudit(
            title=self.title,
            auditor=self.auditor,
            datetime=self.datetime,
            severity=self.max_severity,
            answers=self.answers,
            unresolved_count=self.unresolved_count,
        )
        audit.validate()
        return audit


class CompletedAudit(Document):
    title = StringField(required=True, max_length=TITLE_MAX_LENGTH, min_length=TITLE_MIN_LENGTH)
    auditor = StringField(required=True, max_length=AUDITOR_MAX_LENGTH, min_length=AUDITOR_MIN_LENGTH)
    datetime = DateTimeField(required=True)
    severity = EmbeddedDocumentField(Severity, required=True)
    answers = EmbeddedDocumentListField(Answer, required=True)
    unresolved_count = IntField(required=True, default=0)

    def validate(self, clean=True):
        super().validate(clean)
        unresolved_count = sum(not answer.resolved for answer in self.answers)
        if self.unresolved_count is not unresolved_count:
            raise ValidationError("Resolved answer count " + str(unresolved_count) + " does not match expected count" +
                                  str(self.unresolved_count) + " .")
