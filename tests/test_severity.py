import inspect
import os
import sys
import unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from source.severity import *


class MyTestCase(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
