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

from completed_audit import CompletedAuditBuilder, Answer, Response
from audit_template import Severity


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
