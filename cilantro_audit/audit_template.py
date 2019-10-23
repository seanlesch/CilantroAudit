from mongoengine import Document, StringField, EmbeddedDocument, EmbeddedDocumentField, EmbeddedDocumentListField


class SeverityEnum:
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


class Severity(EmbeddedDocument):
    severity = StringField(required=True)

    @staticmethod
    def default():
        return Severity.green()

    @staticmethod
    def red():
        return Severity(SeverityEnum.RED)

    @staticmethod
    def yellow():
        return Severity(SeverityEnum.YELLOW)

    @staticmethod
    def green():
        return Severity(SeverityEnum.GREEN)

    """
    Cycles through the different options:
    GREEN -> YELLOW -> RED -> GREEN -> ...
    """

    def next(self):
        if SeverityEnum.GREEN == self.severity:
            return Severity.yellow()
        elif SeverityEnum.YELLOW == self.severity:
            return Severity.red()
        else:
            return Severity.green()


class Question(EmbeddedDocument):
    text = StringField(required=True, max_length=50, min_length=1)
    yes = EmbeddedDocumentField(Severity, required=True, default=Severity.default())
    no = EmbeddedDocumentField(Severity, required=True, default=Severity.default())
    other = EmbeddedDocumentField(Severity, required=True, default=Severity.default())


class AuditTemplateBuilder:
    def __init__(self):
        self.title = None
        self.questions = []

    def with_title(self, title):
        self.title = title
        return self

    def with_question(self, question):
        self.questions.append(question)
        return self

    def build(self):
        template = AuditTemplate(title=self.title, questions=self.questions)
        template.validate()
        return template


class AuditTemplate(Document):
    title = StringField(required=True, max_length=50, min_length=1)
    questions = EmbeddedDocumentListField(Question, required=True)
