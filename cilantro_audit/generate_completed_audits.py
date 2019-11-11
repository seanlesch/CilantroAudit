from mongoengine import connect

# import random
# import time

from cilantro_audit.audit_template import Severity, Question, AuditTemplateBuilder
from cilantro_audit.completed_audit import Response, CompletedAuditBuilder, Answer
from cilantro_audit.constants import PROD_DB

db = connect(PROD_DB)
db.drop_database(PROD_DB)

connect(PROD_DB)

if __name__ == '__main__':
    CompletedAuditBuilder() \
        .with_title("") \
        .with_auditor(random.choice(AUDITORS)) \
        .with_answer(random_answer_from_question(q0)) \
        .with_answer(random_answer_from_question(q1)) \
        .with_answer(random_answer_from_question(q2)) \
        .with_answer(random_answer_from_question(q3)) \
        .with_answer(random_answer_from_question(q4)) \
        .build() \
        .save()
