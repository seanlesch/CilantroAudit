import inspect
import os
import sys
import unittest
from mongoengine import ValidationError

# Add the parent directory to the path
# Taken from: https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from source.audit_template_builder import *
from source.question import Question
from mongoengine import ValidationError


class AuditTemplateBuilderTests(unittest.TestCase):
    def test_title_is_required(self):
        self.assertRaises(
            ValidationError,
            AuditTemplateBuilder().with_question(Question(text="Text")).build
        )

    def test_questions_are_required(self):
        self.assertRaises(
            ValidationError,
            AuditTemplateBuilder().with_title("Title").build
        )

    def test_each_question_is_validated(self):
        self.assertRaises(
            ValidationError,
            AuditTemplateBuilder() \
                .with_title("Title") \
                .with_question(Question(text="Title1")) \
                .with_question(Question(text="Title2")) \
                .with_question(Question()) \
                .with_question(Question(text="Title3")) \
                .build
        )

    def test_title_min_length(self):
        self.assertRaises(
            ValidationError,
            AuditTemplateBuilder().with_title("").with_question(Question(text="Text")).build
        )

    def test_title_max_length(self):
        too_many_characters = "PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2f"
        self.assertRaises(
            ValidationError,
            AuditTemplateBuilder() \
                .with_title(too_many_characters) \
                .with_question(Question(text="Text")) \
                .build
        )

    @staticmethod
    def run_tests():
        unittest.main()