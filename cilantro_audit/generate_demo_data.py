from random import choice
from random import randint
from random import shuffle
from datetime import timedelta

from cilantro_audit.audit_template import Severity, Question, AuditTemplateBuilder
from cilantro_audit.completed_audit import Response, CompletedAuditBuilder, Answer
from cilantro_audit.constants import PROD_DB

from mongoengine import connect

db = connect(PROD_DB)
db.drop_database(PROD_DB)
db = connect(PROD_DB)

TITLES = [
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
    "Ink Lap (Upstairs)",
    "Plate Mezzanine",
    "Lab Mezzanine",
    "Finished Goods Warehouse",
    "Blend Room",
    "QC Lap",
    "Mill/Disperser Room Floor",
    "Mill Deck Mezzanine",
    "Mill Room Warehouse",
    "Maintenance",
    "Lift Trucks",
]

TEXTS = [
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

NUM_TEMPLATES = len(TITLES)
NUM_COMPLETED_PER_TEMPLATE = 5
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


def random_titles():
    shuffle(TITLES)


def next_title():
    return TITLES.pop(0)


def random_question():
    return Question(
        text=choice(TEXTS),
        yes=choice(SEVERITIES),
        no=choice(SEVERITIES),
        other=choice(SEVERITIES),
    )


def random_answer_from_question(question):
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


def time_delta(max_years):
    return timedelta(days=randint(0, 31 * 12 * max_years))


if __name__ == '__main__':
    print("\nGenerating", NUM_TEMPLATES, "audit template(s), each with", NUM_COMPLETED_PER_TEMPLATE,
          "completed audit(s), with dates ranging up to", MAX_YEAR_DELTA, "years ago\n...")

    # Shuffle existing titles' list
    random_titles()

    for _ in range(NUM_TEMPLATES):
        title = next_title()
        q0 = random_question()
        q1 = random_question()
        q2 = random_question()
        q3 = random_question()
        q4 = random_question()
        q5 = random_question()
        q6 = random_question()

        AuditTemplateBuilder() \
            .with_title(title) \
            .with_question(q0) \
            .with_question(q1) \
            .with_question(q2) \
            .with_question(q3) \
            .with_question(q4) \
            .with_question(q5) \
            .with_question(q6) \
            .build() \
            .save()

        for _ in range(NUM_COMPLETED_PER_TEMPLATE):
            audit = CompletedAuditBuilder() \
                .with_title(title) \
                .with_auditor(choice(AUDITORS)) \
                .with_answer(random_answer_from_question(q0)) \
                .with_answer(random_answer_from_question(q1)) \
                .with_answer(random_answer_from_question(q2)) \
                .with_answer(random_answer_from_question(q3)) \
                .with_answer(random_answer_from_question(q4)) \
                .with_answer(random_answer_from_question(q5)) \
                .with_answer(random_answer_from_question(q6)) \
                .build()
            audit.datetime -= time_delta(MAX_YEAR_DELTA)
            audit.save()
