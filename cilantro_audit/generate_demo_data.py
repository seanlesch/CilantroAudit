import random
from datetime import timedelta
from itertools import permutations

from mongoengine import connect

from cilantro_audit.audit_template import Severity, Question, AuditTemplateBuilder
from cilantro_audit.completed_audit import Response, CompletedAuditBuilder, Answer
from cilantro_audit.constants import PROD_DB

db = connect(PROD_DB)
db.drop_database(PROD_DB)

connect(PROD_DB)

NUM_TEMPLATES = 25
NUM_COMPLETED_PER_TEMPLATE = 5
MAX_YEAR_DELTA = 4
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def time_delta(max_years):
    return timedelta(days=random.randint(0, 31 * 12 * max_years))


def inverse_factorial(value: int):
    n = 1
    while value > 0:
        n += 1
        value = int(value / n)
    return n


TITLES = ["".join(p) for p in permutations(ALPHABET[0:inverse_factorial(NUM_TEMPLATES)])]

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


def next_title():
    return TITLES.pop(0)


def random_question():
    return Question(
        text=random.choice(TEXTS),
        yes=random.choice(SEVERITIES),
        no=random.choice(SEVERITIES),
        other=random.choice(SEVERITIES),
    )


def random_answer_from_question(question):
    text = question.text
    response = random.choice(RESPONSES)
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
            comment=random.choice(COMMENTS),
        )


if __name__ == '__main__':
    print("\nGenerating", NUM_TEMPLATES, "audit template(s), each with", NUM_COMPLETED_PER_TEMPLATE,
          "completed audit(s), with dates ranging up to", MAX_YEAR_DELTA, "years ago...")
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
                .with_auditor(random.choice(AUDITORS)) \
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
