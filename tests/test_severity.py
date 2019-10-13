import unittest
import sys
sys.path.append("/home/erik/dev/python/CilantroAudit")
from source.severity import *

class MyTestCase(unittest.TestCase):
    def test_default_severity(self):
        self.assertEqual(SeverityEnum.GREEN, Severity.default().severity)

    def test_severity_constructors(self):
        self.assertEqual(SeverityEnum.RED,    Severity(SeverityEnum.RED).severity)
        self.assertEqual(SeverityEnum.YELLOW, Severity(SeverityEnum.YELLOW).severity)
        self.assertEqual(SeverityEnum.GREEN,  Severity(SeverityEnum.GREEN).severity)

if __name__ == '__main__':
    unittest.main()