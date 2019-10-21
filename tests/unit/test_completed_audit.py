import unittest
from datetime import datetime
from mongoengine import ValidationError
from cilantro_audit.audit_template import Severity
from cilantro_audit.completed_audit import CompletedAudit, Answer, Response

VALID_ANSWER = Answer(
    text="Text",
    severity=Severity.red(),
    response=Response.yes(),
)

INVALID_ANSWER = Answer(
    text="Text",
    severity=Severity.red(),
    response=Response.other(),
)


class CompletedAuditTests(unittest.TestCase):
    def test_title_is_required(self):
        self.assertEqual(
            None,
            CompletedAudit(
                title="Title",
                datetime=datetime.now(),
                auditor="Auditor",
                answers=[VALID_ANSWER],
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            CompletedAudit(
                datetime=datetime.now(),
                auditor="Auditor",
                answers=[VALID_ANSWER],
            ).validate
        )

    def test_answers_are_required(self):
        self.assertEqual(
            None,
            CompletedAudit(
                title="Title",
                datetime=datetime.now(),
                auditor="Auditor",
                answers=[VALID_ANSWER],
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            CompletedAudit(
                title="Title",
                datetime=datetime.now(),
                auditor="Auditor",
            ).validate
        )

    def test_each_answer_is_validated(self):
        self.assertEqual(
            None,
            CompletedAudit(
                title="Title",
                datetime=datetime.now(),
                auditor="Auditor",
                answers=[
                    VALID_ANSWER,
                    VALID_ANSWER,
                    VALID_ANSWER,
                    VALID_ANSWER,
                ],
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            CompletedAudit(
                title="Title",
                datetime=datetime.now(),
                auditor="Auditor",
                answers=[
                    VALID_ANSWER,
                    VALID_ANSWER,
                    INVALID_ANSWER,
                    VALID_ANSWER,
                ],
            ).validate
        )

    def test_title_min_length(self):
        character_minimum = "1"
        empty_string = ""
        self.assertEqual(
            None,
            CompletedAudit(
                title=character_minimum,
                datetime=datetime.now(),
                auditor="Auditor",
                answers=[VALID_ANSWER],
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            CompletedAudit(
                title=empty_string,
                datetime=datetime.now(),
                auditor="Auditor",
                answers=[VALID_ANSWER],
            ).validate
        )

    def test_title_max_length(self):
        character_maximum = "PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2"
        too_many_characters = "PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2f"
        self.assertEqual(
            None,
            CompletedAudit(
                title=character_maximum,
                datetime=datetime.now(),
                auditor="Auditor",
                answers=[VALID_ANSWER],
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            CompletedAudit(
                title=too_many_characters,
                datetime=datetime.now(),
                auditor="Auditor",
                answers=[VALID_ANSWER],
            ).validate
        )
