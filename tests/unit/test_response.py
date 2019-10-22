import inspect
import os
import sys
import unittest
from mongoengine import ValidationError

# Add the parent directory to the path
# Taken from: https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
rootdir = os.path.dirname(parentdir)
sys.path.insert(0, os.path.join(rootdir, "source"))

from completed_audit import Response, ResponseEnum


class ResponseTests(unittest.TestCase):
    def test_response_constructors(self):
        self.assertEqual(ResponseEnum.YES, Response.yes().response)
        self.assertEqual(ResponseEnum.NO, Response.no().response)
        self.assertEqual(ResponseEnum.OTHER, Response.other().response)

    def test_response_is_required(self):
        self.assertEqual(None, Response.yes().validate())
        self.assertRaises(ValidationError, Response().validate)

    @staticmethod
    def run_tests():
        unittest.main()
