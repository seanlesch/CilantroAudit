import inspect
import os
import sys
import unittest
from mongoengine import ValidationError

# Add the parent directory to the path
# Taken from: https://stackoverflow.com/answers/714063/importing-modules-from-parent-folder
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
rootdir = os.path.dirname(parentdir)
sys.path.insert(0, os.path.join(rootdir, "source"))

from completed_audit import Answer, Response
from audit_template import Severity


class AnswerTests(unittest.TestCase):
    def test_answer_construction(self):
        expected_text = "Expected Text"
        expected_severity = Severity.red()
        expected_response = Response.yes()
        expected_comments = "Expected Comments"

        answer = Answer(
            text=expected_text,
            severity=expected_severity,
            response=expected_response,
            comments=expected_comments,
        )

        self.assertEqual(expected_text, answer.text)
        self.assertEqual(expected_severity, answer.severity)
        self.assertEqual(expected_response, answer.response)
        self.assertEqual(expected_comments, answer.comments)

    def test_comments_required_only_for_other_response(self):
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
        other_answer_without_comments = Answer(
            text="Text",
            severity=Severity.green(),
            response=Response.other(),
        )
        other_answer_with_comments = Answer(
            text="Text",
            severity=Severity.yellow(),
            response=Response.other(),
            comments="Comments"
        )
        self.assertEqual(None, yes_answer.validate())
        self.assertEqual(None, no_answer.validate())
        self.assertEqual(None, other_answer_with_comments.validate())
        self.assertRaises(ValidationError, other_answer_without_comments.validate)

    def test_severity_is_required(self):
        self.assertEqual(
            None,
            Answer(
                text="With Text",
                severity=Severity.red(),
                response=Response.yes(),
            ).validate()
        )
        self.assertRaises(ValidationError, Answer(
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
        self.assertRaises(ValidationError, Answer(
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
        self.assertRaises(ValidationError, Answer(
            severity=Severity.red(),
            response=Response.yes(),
        ).validate
                          )

    def test_text_max_length(self):
        character_limit = "PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2"
        character_maximum = "PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2f"
        self.assertEqual(
            None,
            Answer(
                text=character_limit,
                severity=Severity.red(),
                response=Response.yes(),
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            Answer(
                text=character_maximum,
                severity=Severity.red(),
                response=Response.yes(),
            ).validate
        )

    def test_text_min_length(self):
        character_minimum = "."
        empty_string = ""
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
                text=empty_string,
                severity=Severity.red(),
                response=Response.yes(),
            ).validate
        )

    def test_comments_max_length(self):
        character_limit = "PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2"
        character_maximum = "PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh22"
        self.assertEqual(
            None,
            Answer(
                text="With Text",
                severity=Severity.red(),
                response=Response.other(),
                comments=character_limit,
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            Answer(
                text="With Text",
                severity=Severity.red(),
                response=Response.other(),
                comments=character_maximum,
            ).validate
        )

    def test_comments_min_length(self):
        character_minimum = "."
        empty_string = ""
        self.assertEqual(
            None,
            Answer(
                text="With Text",
                severity=Severity.red(),
                response=Response.other(),
                comments=character_minimum,
            ).validate()
        )
        self.assertRaises(
            ValidationError,
            Answer(
                text="With Text",
                severity=Severity.red(),
                response=Response.other(),
                comments=empty_string,
            ).validate
        )

    @staticmethod
    def run_tests():
        unittest.main()
