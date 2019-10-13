from mongoengine import EmbeddedDocument, StringField


class SeverityEnum:
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


class Severity(EmbeddedDocument):
    severity = StringField(required=True)

    def __init__(self, *args, **values):
        super().__init__(*args, **values)

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

    def next(self):
        if SeverityEnum.GREEN == self.severity:
            return Severity.yellow()
        elif SeverityEnum.YELLOW == self.severity:
            return Severity.red()
        else:
            return Severity.green()
