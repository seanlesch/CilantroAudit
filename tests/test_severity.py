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

from audit_template import Severity, SeverityEnum


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

    @staticmethod
    def run_tests():
        unittest.main()
