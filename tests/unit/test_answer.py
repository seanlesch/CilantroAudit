import unittest

from mongoengine import ValidationError

from cilantro_audit.audit_template import Severity
from cilantro_audit.completed_audit import Answer, Response
from cilantro_audit.constants import TEXT_MAX_LENGTH, COMMENT_MAX_LENGTH, TEXT_MIN_LENGTH, COMMENT_MIN_LENGTH


class AnswerTests(unittest.TestCase):
    def test_answer_construction(self):
        expected_text = "Expected Text"
        expected_severity = Severity.red()
        expected_response = Response.yes()
        expected_comment = "Expected Comments"
        expected_resolved = True

        answer = Answer(
            text=expected_text,
            severity=expected_severity,
            response=expected_response,
            comment=expected_comment,
        )

        self.assertEqual(expected_text, answer.text)
        self.assertEqual(expected_severity, answer.severity)
        self.assertEqual(expected_response, answer.response)
        self.assertEqual(expected_comment, answer.comment)
        self.assertEqual(expected_resolved, answer.resolved)

    def test_comment_required_only_for_other_response(self):
        yes_answer = Answer(
            text="Text",
            severity=Severity.red(),
            response=Response.yes(),
        )
        no_answer = Answer(
            text="Text",
            severity=Severity.yellow(),
            response=Response.no(),
        )
        other_answer_without_comment = Answer(
            text="Text",
            severity=Severity.green(),
            response=Response.other(),
        )
        other_answer_with_comment = Answer(
            text="Text",
            severity=Severity.yellow(),
            response=Response.other(),
            comment="Comments"
        )
        self.assertEqual(None, yes_answer.validate())
        self.assertEqual(None, no_answer.validate())
        self.assertEqual(None, other_answer_with_comment.validate())
        self.assertRaises(ValidationError, other_answer_without_comment.validate)

    def test_severity_is_required(self):
        self.assertEqual(
            None,
            Answer(
                text="With Text",
                severity=Severity.red(),
                response=Response.yes(),
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            Answer(
                text="With Text",
                response=Response.yes(),
            ).validate
        )

    def test_response_is_required(self):
        self.assertEqual(
            None,
            Answer(
                text="With Text",
                severity=Severity.red(),
                response=Response.yes(),
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            Answer(
                text="With Text",
                severity=Severity.red(),
            ).validate
        )

    def test_text_is_required(self):
        self.assertEqual(
            None,
            Answer(
                text="With Text",
                severity=Severity.red(),
                response=Response.yes(),
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            Answer(
                severity=Severity.red(),
                response=Response.yes(),
            ).validate
        )

    def test_text_max_length(self):
        character_maximum = ""
        too_many_characters = "a"
        for _ in range(0, TEXT_MAX_LENGTH):
            character_maximum += "a"
            too_many_characters += "a"
        self.assertEqual(
            None,
            Answer(
                text=character_maximum,
                severity=Severity.red(),
                response=Response.yes(),
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            Answer(
                text=too_many_characters,
                severity=Severity.red(),
                response=Response.yes(),
            ).validate
        )

    def test_text_min_length(self):
        character_minimum = ""
        for _ in range(0, TEXT_MIN_LENGTH):
            character_minimum += "a"
        too_few_characters = character_minimum[1:]
        self.assertEqual(
            None,
            Answer(
                text=character_minimum,
                severity=Severity.red(),
                response=Response.yes(),
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            Answer(
                text=too_few_characters,
                severity=Severity.red(),
                response=Response.yes(),
            ).validate
        )

    def test_comment_max_length(self):
        character_maximum = ""
        too_many_characters = "a"
        for _ in range(0, COMMENT_MAX_LENGTH):
            character_maximum += "a"
            too_many_characters += "a"
        self.assertEqual(
            None,
            Answer(
                text="With Text",
                severity=Severity.red(),
                response=Response.other(),
                comment=character_maximum,
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            Answer(
                text="With Text",
                severity=Severity.red(),
                response=Response.other(),
                comment=too_many_characters,
            ).validate
        )

    def test_comment_min_length(self):
        character_minimum = ""
        for _ in range(0, COMMENT_MIN_LENGTH):
            character_minimum += "a"
        too_few_characters = character_minimum[1:]
        self.assertEqual(
            None,
            Answer(
                text="With Text",
                severity=Severity.red(),
                response=Response.other(),
                comment=character_minimum,
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            Answer(
                text="With Text",
                severity=Severity.red(),
                response=Response.other(),
                comment=too_few_characters,
            ).validate
        )
