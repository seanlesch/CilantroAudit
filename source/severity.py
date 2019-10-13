from mongoengine import *

class SeverityEnum:
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


class Severity(Document):
    severity = StringField(required=True)

    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    @staticmethod
    def default():
        return Severity(SeverityEnum.GREEN)
