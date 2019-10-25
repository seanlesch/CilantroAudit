import unittest
from mongoengine import ValidationError
from cilantro_audit.audit_template import Question, Severity
from cilantro_audit.constants import QUESTION_MAX_LENGTH


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
        character_maximum = ""
        too_many_characters = "a"
        for _ in range(0, QUESTION_MAX_LENGTH):
            character_maximum += "a"
            too_many_characters += "a"
        self.assertEqual(None, Question(text=character_maximum).validate())
        self.assertRaises(ValidationError, Question(text=too_many_characters).validate)

    def test_text_min_length(self):
        character_minimum = "."
        empty_string = ""
        self.assertEqual(None, Question(text=character_minimum).validate())
        self.assertRaises(ValidationError, Question(text=empty_string).validate)
