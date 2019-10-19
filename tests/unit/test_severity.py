import unittest
from mongoengine import ValidationError
from cilantro_audit.audit_template import Severity, SeverityEnum


class SeverityTests(unittest.TestCase):
    def test_default_severity(self):
        self.assertEqual(SeverityEnum.GREEN, Severity.default().severity)

    def test_severity_constructors(self):
        self.assertEqual(SeverityEnum.RED, Severity.red().severity)
        self.assertEqual(SeverityEnum.YELLOW, Severity.yellow().severity)
        self.assertEqual(SeverityEnum.GREEN, Severity.green().severity)

    def test_severity_is_required(self):
        self.assertEqual(None, Severity.default().validate())
        self.assertRaises(ValidationError, Severity().validate)

    def test_next_severity(self):
        self.assertEqual(Severity.yellow(), Severity.green().next())
        self.assertEqual(Severity.red(), Severity.yellow().next())
        self.assertEqual(Severity.green(), Severity.red().next())
