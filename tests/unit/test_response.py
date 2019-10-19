import unittest
from mongoengine import ValidationError
from cilantro_audit.completed_audit import Response, ResponseEnum


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
