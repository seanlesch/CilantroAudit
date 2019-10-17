import inspect
import os
import sys
import unittest
from datetime import datetime
from mongoengine import connect

# Add the parent directory to the path
# Taken from: https://stackoverflow.com/answers/714063/importing-modules-from-parent-folder
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
rootdir = os.path.dirname(parentdir)
sys.path.insert(0, os.path.join(rootdir, "source"))

from completed_audit import CompletedAudit, CompletedAuditBuilder, Answer, Response
from audit_template import Severity

connect("testdb")

class CompletedAuditTests(unittest.TestCase):

    def __del__(self):
        db = connect("testdb")
        db.drop_database("testdb")

    def test_storage_and_retrieval(self):
        title = "Boiler Room Shenanigans"
        auditor = "Erik The Auditor"

        a0_text = "Did you stick your head in the boiler?"
        a0_severity = Severity.red()
        a0_response = Response.yes()

        a1_text = "Was there dust on the machine?"
        a1_severity = Severity.yellow()
        a1_response = Response.no()

        a2_text = "Did you clean the machine?"
        a2_severity = Severity.green()
        a2_response = Response.other()
        a2_comments = "There was no dust on the machine to clean."

        CompletedAuditBuilder() \
            .with_title(title) \
            .with_auditor(auditor) \
            .with_answer(
                Answer(
                    text=a0_text,
                    severity=a0_severity,
                    response=a0_response,
                )
            ).with_answer(
                Answer(
                    text=a1_text,
                    severity=a1_severity,
                    response=a1_response,
                )
            ).with_answer(
                Answer(
                    text=a2_text,
                    severity=a2_severity,
                    response=a2_response,
                    comments=a2_comments,
                )
            ).build().save()

        audits = CompletedAudit.objects(title=title)

        self.assertEqual(title, audits[0].title)
        self.assertEqual(1, len(audits))
        self.assertEqual(3, len(audits[0].answers))

        audit = audits[0]

        a0_text = "Did you stick your head in the boiler?"
        a0_severity = Severity.red()
        a0_response = Response.yes()

        a1_text = "Was there dust on the machine?"
        a1_severity = Severity.yellow()
        a1_response = Response.no()

        a2_text = "Did you clean the machine?"
        a2_severity = Severity.green()
        a2_response = Response.other()
        a2_comments = "There was no dust on the machine to clean."

        self.assertEqual(a0_text, audit.answers[0].text)
        self.assertEqual(a0_severity, audit.answers[0].severity)
        self.assertEqual(a0_response, audit.answers[0].response)
        self.assertEqual(None, audit.answers[0].comments)

        self.assertEqual(a1_text, audit.answers[1].text)
        self.assertEqual(a1_severity, audit.answers[1].severity)
        self.assertEqual(a1_response, audit.answers[1].response)
        self.assertEqual(None, audit.answers[1].comments)

        self.assertEqual(a2_text, audit.answers[2].text)
        self.assertEqual(a2_severity, audit.answers[2].severity)
        self.assertEqual(a2_response, audit.answers[2].response)
        self.assertEqual(a2_comments, audit.answers[2].comments)

        self.assertGreaterEqual(datetime.utcnow(), audit.datetime)


