import inspect
import os
import sys
import unittest
from mongoengine import ValidationError

# Add the parent directory to the path
# Taken from: https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, os.path.join(parentdir, "source"))

from question import *


class QuestionTests(unittest.TestCase):
    def test_question_with_text(self):
        expected = "Question Text"
        question = Question(text=expected)
        self.assertEqual(expected, question.text)

    def test_default_severities(self):
        question = Question(text="Question Text")
        self.assertEqual(Severity.green(), question.yes)
        self.assertEqual(Severity.green(), question.no)
        self.assertEqual(Severity.green(), question.other)

    def test_custom_severities(self):
        question = Question(
            text="Question Text",
            yes=Severity.red(),
            no=Severity.yellow(),
            other=Severity.green(),
        )
        self.assertEqual(Severity.red(), question.yes)
        self.assertEqual(Severity.yellow(), question.no)
        self.assertEqual(Severity.green(), question.other)

    def test_text_is_required(self):
        self.assertEqual(None, Question(text="With Text").validate())
        self.assertRaises(ValidationError, Question().validate)

    def test_text_max_length(self):
        fifty_characters = "PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2"
        too_many_characters = "PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2f"
        self.assertEqual(None, Question(text=fifty_characters).validate())
        self.assertRaises(ValidationError, Question(text=too_many_characters).validate)

    def test_text_min_length(self):
        one_character = "."
        empty_string = ""
        self.assertEqual(None, Question(text=one_character).validate())
        self.assertRaises(ValidationError, Question(text=empty_string).validate)

    @staticmethod
    def run_tests():
        unittest.main()
