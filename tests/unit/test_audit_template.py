import unittest
from mongoengine import ValidationError
from cilantro_audit.audit_template import AuditTemplate, Question


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
        character_maximum = "PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2"
        too_many_characters = "PM4t5qKhqS6oSEtPrtXUaQWbEeZ2ITca4AsSzF2KApecyI6Yh2f"
        self.assertEqual(None, AuditTemplate(title=character_maximum, questions=[Question(text="Text")]).validate())
        self.assertRaises(ValidationError,
                          AuditTemplate(title=too_many_characters, questions=[Question(text="Text")]).validate)
