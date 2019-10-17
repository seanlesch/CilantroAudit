import inspect
import os
import sys
import unittest
from mongoengine import connect, get_db

# Add the parent directory to the path
# Taken from: https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
rootdir = os.path.dirname(parentdir)
sys.path.insert(0, os.path.join(rootdir, "source"))

from audit_template import AuditTemplate, AuditTemplateBuilder, Question, Severity

connect("testdb")

class AuditTemplateTests(unittest.TestCase):

    def __del__(self):
        db = connect("testdb")
        db.drop_database("testdb")

    def test_storage_and_retrieval(self):
        title = "Test Storage And Retrieval"
        q0_text = "Question 0"
        q1_text = "Question 1"
        q2_text = "Question 2"
        question0 = Question(text=q0_text)

        question1 = Question(text=q1_text, yes=Severity.red())

        question2 = Question(text=q2_text, no=Severity.red(), other=Severity.yellow())

        AuditTemplateBuilder() \
            .with_title(title) \
            .with_question(question0) \
            .with_question(question1) \
            .with_question(question2) \
            .build() \
            .save()

        templates = AuditTemplate.objects(title=title)

        self.assertEqual(title, templates[0].title)
        self.assertEqual(1, len(templates))
        self.assertEqual(3, len(templates[0].questions))

        self.assertEqual(q0_text, templates[0].questions[0].text)
        self.assertEqual(Severity.green(), templates[0].questions[0].yes)
        self.assertEqual(Severity.green(), templates[0].questions[0].no)
        self.assertEqual(Severity.green(), templates[0].questions[0].other)

        self.assertEqual(q1_text, templates[0].questions[1].text)
        self.assertEqual(Severity.red(),   templates[0].questions[1].yes)
        self.assertEqual(Severity.green(), templates[0].questions[1].no)
        self.assertEqual(Severity.green(), templates[0].questions[1].other)

        self.assertEqual(q2_text, templates[0].questions[2].text)
        self.assertEqual(Severity.green(),  templates[0].questions[2].yes)
        self.assertEqual(Severity.red(),    templates[0].questions[2].no)
        self.assertEqual(Severity.yellow(), templates[0].questions[2].other)
