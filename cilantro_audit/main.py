# from audit_template import AuditTemplateBuilder, Question, Severity
from audit_template import Severity
from completed_audit import CompletedAudit, CompletedAuditBuilder, Answer, Response
from mongoengine import connect, ValidationError

connect("troast")

if __name__ == '__main__':
    try:
        CompletedAuditBuilder() \
            .with_title("Boiler Room Shenanigans") \
            .with_auditor("Jimmy Johns") \
            .with_answer(
            Answer(
                text="Did you stick your head in the boiler?",
                severity=Severity.red(),
                response=Response.yes(),
            )
        ).with_answer(
            Answer(
                text="Was there dust on the machine?",
                response=Response.no(),
                severity=Severity.green(),
            )
        ).with_answer(
            Answer(
                text="Did you clean the machine?",
                response=Response.other(),
                severity=Severity.yellow(),
            )
        ).build().save()
    except ValidationError as error:
        print(error.message)
