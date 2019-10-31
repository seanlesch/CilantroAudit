import unittest

from mongoengine import ValidationError

from cilantro_audit.audit_template import AuditTemplate, Question
from cilantro_audit.constants import TITLE_MAX_LENGTH


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
        character_maximum = ""
        too_many_characters = "a"
        for _ in range(0, TITLE_MAX_LENGTH):
            character_maximum += "a"
            too_many_characters += "a"
        self.assertEqual(None, AuditTemplate(title=character_maximum, questions=[Question(text="Text")]).validate())
        self.assertRaises(ValidationError,
                          AuditTemplate(title=too_many_characters, questions=[Question(text="Text")]).validate)
