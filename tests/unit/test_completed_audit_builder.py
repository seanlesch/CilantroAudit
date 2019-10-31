import unittest
from datetime import datetime

from mongoengine import ValidationError

from cilantro_audit.audit_template import Severity
from cilantro_audit.completed_audit import CompletedAuditBuilder, Answer, Response

VALID_ANSWER = Answer(
    text="Text",
    severity=Severity.red(),
    response=Response.yes(),
)

GREEN_ANSWER = Answer(
    text="Green Answer",
    severity=Severity.green(),
    response=Response.yes(),
)

YELLOW_ANSWER = Answer(
    text="Yellow Answer",
    severity=Severity.yellow(),
    response=Response.other(),
    comment="Toast",
)

RED_ANSWER = Answer(
    text="Red Answer",
    severity=Severity.red(),
    response=Response.no(),
)

INVALID_ANSWER = Answer(
    text="Text",
    severity=Severity.red(),
    response=Response.other(),
)


class CompletedAuditBuilderTests(unittest.TestCase):
    def test_title_is_required(self):
        builder = CompletedAuditBuilder() \
            .with_auditor("Auditor") \
            .with_answer(VALID_ANSWER)
        self.assertRaises(ValidationError, builder.build)

    def test_auditor_is_required(self):
        builder = CompletedAuditBuilder() \
            .with_title("Title") \
            .with_answer(VALID_ANSWER)
        self.assertRaises(ValidationError, builder.build)

    def test_answers_are_required(self):
        builder = CompletedAuditBuilder() \
            .with_title("Title") \
            .with_auditor("Auditor")
        self.assertRaises(ValidationError, builder.build)

    def test_each_answer_is_validated(self):
        builder = CompletedAuditBuilder() \
            .with_title("Title") \
            .with_auditor("Auditor") \
            .with_answer(VALID_ANSWER) \
            .with_answer(VALID_ANSWER) \
            .with_answer(INVALID_ANSWER) \
            .with_answer(VALID_ANSWER)
        self.assertRaises(ValidationError, builder.build)

    def test_title_min_length(self):
        empty_string = ""
        builder = CompletedAuditBuilder() \
            .with_title(empty_string) \
            .with_auditor("Auditor") \
            .with_answer(VALID_ANSWER)
        self.assertRaises(ValidationError, builder.build)

    def test_title_max_length(self):
        too_many_characters = "PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2f"
        builder = CompletedAuditBuilder() \
            .with_title(too_many_characters) \
            .with_auditor("Auditor") \
            .with_answer(VALID_ANSWER)
        self.assertRaises(ValidationError, builder.build)

    def test_datetime_stamp(self):
        audit = CompletedAuditBuilder() \
            .with_title("Title") \
            .with_auditor("Auditor") \
            .with_answer(VALID_ANSWER) \
            .build()
        self.assertGreaterEqual(datetime.utcnow(), audit.datetime)

    def test_max_severity_green(self):
        audit = CompletedAuditBuilder() \
            .with_title("Title") \
            .with_auditor("Auditor") \
            .with_answer(GREEN_ANSWER) \
            .with_answer(GREEN_ANSWER) \
            .with_answer(GREEN_ANSWER) \
            .build()
        self.assertEqual(Severity.green(), audit.severity)

    def test_max_severity_yellow(self):
        audit = CompletedAuditBuilder() \
            .with_title("Title") \
            .with_auditor("Auditor") \
            .with_answer(GREEN_ANSWER) \
            .with_answer(GREEN_ANSWER) \
            .with_answer(YELLOW_ANSWER) \
            .with_answer(GREEN_ANSWER) \
            .build()
        self.assertEqual(Severity.yellow(), audit.severity)

    def test_max_severity_yellow(self):
        audit = CompletedAuditBuilder() \
            .with_title("Title") \
            .with_auditor("Auditor") \
            .with_answer(GREEN_ANSWER) \
            .with_answer(RED_ANSWER) \
            .with_answer(GREEN_ANSWER) \
            .with_answer(YELLOW_ANSWER) \
            .with_answer(GREEN_ANSWER) \
            .build()
        self.assertEqual(Severity.red(), audit.severity)
        audit = CompletedAuditBuilder() \
            .with_title("Title") \
            .with_auditor("Auditor") \
            .with_answer(GREEN_ANSWER) \
            .with_answer(YELLOW_ANSWER) \
            .with_answer(GREEN_ANSWER) \
            .with_answer(RED_ANSWER) \
            .with_answer(GREEN_ANSWER) \
            .build()
        self.assertEqual(Severity.red(), audit.severity)
        audit = CompletedAuditBuilder() \
            .with_title("Title") \
            .with_auditor("Auditor") \
            .with_answer(GREEN_ANSWER) \
            .with_answer(GREEN_ANSWER) \
            .with_answer(RED_ANSWER) \
            .with_answer(GREEN_ANSWER) \
            .build()
        self.assertEqual(Severity.red(), audit.severity)

