from mongoengine import *

severities = {"RED", "YELLOW", "GREEN"}

class SeverityEnum:
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


class Severity(Document):
    severity = StringField(required=True)

    @staticmethod
    def default():
        return Severity(SeverityEnum.GREEN)
