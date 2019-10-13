import inspect
import os
import sys
import unittest

# Add the parent directory to the path
# Taken from: https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from source.audit_template import *


class AuditTemplateTests(unittest.TestCase):
    def test_title_is_required(self):
        self.assertEqual(None, AuditTemplate(title="Title", questions=[Question(text="Text")]).validate())
        self.assertRaises(ValidationError, AuditTemplate(questions=[Question(text="Text")]).validate)

    def test_questions_are_required(self):
        self.assertEqual(None, AuditTemplate(title="Title", questions=[Question(text="Text")]).validate())
        self.assertRaises(ValidationError, AuditTemplate(title="Title").validate)

    def test_each_question_is_validated(self):
        self.assertEqual(None, AuditTemplate(title="Title", questions=[Question(text="Text")]).validate())
        self.assertRaises(ValidationError, AuditTemplate(
            title="Title",
            questions=[
                Question(text="Title1"),
                Question(text="Title2"),
                Question(),
                Question(text="Title2"),
            ]
        ).validate)

    def test_title_min_length(self):
        self.assertEqual(None, AuditTemplate(title="Title", questions=[Question(text="Text")]).validate())
        self.assertRaises(ValidationError, AuditTemplate(title="", questions=[Question(text="Text")]).validate)

    def test_title_max_length(self):
        fifty_characters = "PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2"
        too_many_characters = "PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2f"
        self.assertEqual(None, AuditTemplate(title=fifty_characters, questions=[Question(text="Text")]).validate())
        self.assertRaises(ValidationError,
                          AuditTemplate(title=too_many_characters, questions=[Question(text="Text")]).validate)

    @staticmethod
    def run_tests():
        unittest.main()
