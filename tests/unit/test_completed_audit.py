import unittest
from datetime import datetime

from mongoengine import ValidationError

from cilantro_audit.audit_template import Severity
from cilantro_audit.completed_audit import CompletedAudit, Answer, Response
from cilantro_audit.constants import TITLE_MAX_LENGTH, TITLE_MIN_LENGTH

VALID_ANSWER = Answer(
    text="Text",
    severity=Severity.red(),
    resolved=False,
    response=Response.yes(),
)

OTHER_NO_COMMENT_ANSWER = Answer(
    text="Text",
    severity=Severity.red(),
    resolved=False,
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
                severity=Severity.green(),
                unresolved_count=1,
                answers=[VALID_ANSWER],
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            CompletedAudit(
                datetime=datetime.now(),
                auditor="Auditor",
                severity=Severity.green(),
                unresolved_count=1,
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
                severity=Severity.green(),
                unresolved_count=1,
                answers=[VALID_ANSWER],
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            CompletedAudit(
                title="Title",
                datetime=datetime.now(),
                auditor="Auditor",
                severity=Severity.green(),
            ).validate
        )

    def test_each_answer_is_validated(self):
        self.assertEqual(
            None,
            CompletedAudit(
                title="Title",
                datetime=datetime.now(),
                auditor="Auditor",
                severity=Severity.green(),
                unresolved_count=4,
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
                severity=Severity.green(),
                unresolved_count=4,
                answers=[
                    VALID_ANSWER,
                    VALID_ANSWER,
                    OTHER_NO_COMMENT_ANSWER,
                    VALID_ANSWER,
                ],
            ).validate
        )

    def test_title_min_length(self):
        character_minimum = ""
        for _ in range(0, TITLE_MIN_LENGTH):
            character_minimum += "a"
        too_few_characters = character_minimum[1:]
        self.assertEqual(
            None,
            CompletedAudit(
                title=character_minimum,
                datetime=datetime.now(),
                auditor="Auditor",
                severity=Severity.green(),
                unresolved_count=1,
                answers=[VALID_ANSWER],
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            CompletedAudit(
                title=too_few_characters,
                datetime=datetime.now(),
                auditor="Auditor",
                severity=Severity.green(),
                unresolved_count=1,
                answers=[VALID_ANSWER],
            ).validate
        )

    def test_title_max_length(self):
        character_maximum = ""
        too_many_characters = "a"
        for _ in range(0, TITLE_MAX_LENGTH):
            character_maximum += "a"
            too_many_characters += "a"
        self.assertEqual(
            None,
            CompletedAudit(
                title=character_maximum,
                datetime=datetime.now(),
                auditor="Auditor",
                severity=Severity.green(),
                unresolved_count=1,
                answers=[VALID_ANSWER],
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            CompletedAudit(
                title=too_many_characters,
                datetime=datetime.now(),
                auditor="Auditor",
                severity=Severity.green(),
                unresolved_count=1,
                answers=[VALID_ANSWER],
            ).validate
        )

    def test_unresolved_count_matches_unresolved_answers(self):
        self.assertEqual(
            None,
            CompletedAudit(
                title="Title",
                datetime=datetime.now(),
                auditor="Auditor",
                severity=Severity.green(),
                unresolved_count=4,
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
                severity=Severity.green(),
                answers=[
                    VALID_ANSWER,
                    VALID_ANSWER,
                    VALID_ANSWER,
                    VALID_ANSWER,
                ],
            ).validate
        )
