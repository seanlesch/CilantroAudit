#from audit_template import AuditTemplateBuilder, Question, Severity
from audit_template import Severity
from completed_audit import CompletedAudit, Answer, Response
from datetime import datetime
from mongoengine import connect

connect("troast")


if __name__ == '__main__':

    CompletedAudit(
        title="Boiler Room Shenanigans",
        datetime=datetime.utcnow(),
        auditor="Erik Nordin",
        answers=[
            Answer(
                text="Did you stick your head in the boiler?",
                response=Response.yes(),
                severity=Severity.red(),
            ),
            Answer(
                text="Was there dust on the machine?",
                response=Response.no(),
                severity=Severity.green(),
            ),
            Answer(
                text="Did you clean the machine?",
                response=Response.other(),
                severity=Severity.yellow(),
                comments="There was no dust on the machine, so I didn't clean it."
            )
        ]
    ).save()
