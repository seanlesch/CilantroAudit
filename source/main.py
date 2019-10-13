from question import Question
from severity import Severity
from audit_template_builder import AuditTemplateBuilder
from mongoengine import connect

connect("toast")

if __name__ == '__main__':
    question1 = Question(text="Was there dust on the thing?")

    question2 = Question(
        text="Did you stick your head in the boiler?",
        yes=Severity.red(),
    )

    question3 = Question(
        text="Did you clean the boiler today?",
        no=Severity.red(),
        other=Severity.yellow(),
    )

    AuditTemplateBuilder() \
        .with_title("Boiler Room Shenanigans") \
        .with_question(question1) \
        .with_question(question2) \
        .with_question(question3) \
        .build() \
        .save()



