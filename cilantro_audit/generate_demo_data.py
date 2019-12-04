from random import sample
from random import choice
from random import randint
from random import shuffle
from random import randrange

from datetime import datetime
from datetime import timedelta

from cilantro_audit.audit_template import Severity, Question, AuditTemplateBuilder, AuditTemplate
from cilantro_audit.completed_audit import Response, CompletedAuditBuilder, Answer, CompletedAudit
from cilantro_audit.constants import PROD_DB

from mongoengine import connect

connect(PROD_DB)

AUDITORS = [
    "Piers Thompson",
    "Russell Hayes",
    "Kade Saunders",
    "Delores Wright",
    "Matei Prosser",
    "Sinead Mcnamara",
    "Sila Blake",
    "Aislinn Pace",
    "Ismail Wells",
    "Ikrah Tapia",
    "Nell Lim",
    "Damian Fry",
    "Jaya Mills",
    "Tai Sargent",
    "Elizabeth Bentley",
    "Wren O'Moore",
    "Justin Lawson",
    "Regina Mcculloch",
    "Liberty Padilla",
    "Jenson Wilkerson",
]

AUDIT_TITLES = [
    "Outside Break Area (Off South Porch)",
    "Offices",
    "Basement (Storage and Meeting Rooms)",
    "Basement - Computer Room",
    "Art Department",
    "Camera Department",
    "Plate Department",
    "Mounting Department",
    "Plate Warehouse",
    "Plant Lunchroom",
    "Front Office Lunchroom",
    "Office Area Men's Room",
    "Men's Locker Room",
    "Common Area",
    "Office Area Lady's Room",
    "Lady's Locker Room",
    "Outside Basement Door Area",
    "Beckart Working Area",
    "Dumpster Areas",
    "Flammable Storage Room (EPR)",
    "Shipping/Receiving",
    "Recycler Room (Next to Maintenance)",
    "Compressor Room (Next to Maintenance)",
    "Ink Lab (Upstairs)",
    "Plate Mezzanine",
    "Lab Mezzanine",
    "Finished Goods Warehouse",
    "Blend Room",
    "QC Lab",
    "Mill/Disperser Room Floor",
    "Mill Deck Mezzanine",
    "Mill Room Warehouse",
    "Maintenance",
    "Lift Trucks",
]

QUESTION_TEXTS = [
    "Who's the best auditor in town!? Is it you?",
    "Will you clean the thing today?",
    "Will you clean the thing tomorrow?",
    "Did you check the stuff?",
    "Do you check the stuff every day?",
    "Was someone ice skating on the floor?",
    "Was someone lighting inflammable things on fire?",
    "Were you the one lighting things on fire?",
    "Did you let the catered lunch get cold?",
    "Did you keep the catered lunch warm?",
]

COMMENTS = [
    "I simply forgot today.",
    "It should have been done already.",
    "Oh... I was supposed to do that?",
    "Oh yeah, it's done. I just didn't check it off.",
    "Where am I, again?",
    "Who's line is it, anyway? Cilantro!",
    "Oh, now I understand. Can we escalate this to a manager?",
    "I always complete my tasks on time.",
    "This is my favorite part of my job.",
    "Does anyone read this feedback?",
]

NUM_TEMPLATES = len(AUDIT_TITLES)
NUM_RESPONSES = randrange(1, len(AUDITORS))
MAX_YEAR_DELTA = 4

SEVERITIES = [
    Severity.red(),
    Severity.yellow(),
    Severity.yellow(),
    Severity.yellow(),
    Severity.green(),
    Severity.green(),
    Severity.green(),
    Severity.green(),
    Severity.green(),
    Severity.green(),
    Severity.green(),
    Severity.green(),
]

RESPONSES = [
    Response.yes(),
    Response.no(),
    Response.other(),
]


def get_question(question_text):
    return Question(
        text=question_text,
        yes=choice(SEVERITIES),
        no=choice(SEVERITIES),
        other=choice(SEVERITIES),
    )


def get_random_answer_for(question):
    response = choice(RESPONSES)
    if Response.yes() == response:
        return Answer(
            text=question.text,
            severity=question.yes,
            response=response,
        )
    elif Response.no() == response:
        return Answer(
            text=question.text,
            severity=question.no,
            response=response,
        )
    elif Response.other() == response:
        return Answer(
            text=question.text,
            severity=question.yes,
            response=response,
            comment=choice(COMMENTS),
        )


if __name__ == '__main__':
    print("\nGenerating", NUM_TEMPLATES, "AuditTemplate(s), each with", NUM_RESPONSES,
          "CompletedAudit(s) dated up to", MAX_YEAR_DELTA, "years ago.\n...")

    AuditTemplate.objects.delete()
    CompletedAudit.objects.delete()

    # Randomize Data
    shuffle(AUDIT_TITLES)
    shuffle(COMMENTS)

    # Create an AuditTemplate for each Audit Title and assign x-number of CompletedAudits (Responses) to it
    for title in AUDIT_TITLES:
        template_audit = AuditTemplateBuilder().with_title(title)

        # Use a variable number of random questions for each template and add them to this Audit Template
        rand_questions_list = []
        for question_text in sample(QUESTION_TEXTS, randrange(1, len(QUESTION_TEXTS))):
            q = get_question(question_text)
            rand_questions_list.append(q)
            template_audit.with_question(q)

        template_audit.build().save()

        # Assign a variable number of CompletedAudits (Responses) to this template (no duplicate auditors)
        for unique_auditor in sample(AUDITORS, NUM_RESPONSES):
            completed_audit = CompletedAuditBuilder() \
                .with_title(title) \
                .with_auditor(unique_auditor) \
                .with_datetime(datetime.utcnow() - timedelta(days=randint(0, (31 * 12 * MAX_YEAR_DELTA)),
                                                             hours=randint(0, 24),
                                                             minutes=randint(0, 60),
                                                             seconds=randint(0, 60)))

            for rand_question in rand_questions_list:
                completed_audit.with_answer(get_random_answer_for(rand_question))

            completed_audit.build().save()
