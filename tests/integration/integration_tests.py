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
        question1 = Question(text="Question 0")

        question2 = Question(text="Question 1", yes=Severity.red())

        question3 = Question(text="Question 2", no=Severity.red(), other=Severity.yellow())

        AuditTemplateBuilder() \
            .with_title(title) \
            .with_question(question1) \
            .with_question(question2) \
            .with_question(question3) \
            .build() \
            .save()

        self.assertEqual(1, AuditTemplate.objects[:1](title=title).count())
        for template in AuditTemplate.objects[:1](title=title):
            self.assertEqual(title, template.title)
            self.assertEqual("Question 0", template.questions[0].text)
            self.assertEqual("Question 1", template.questions[1].text)
            self.assertEqual("Question 2", template.questions[2].text)

if __name__ == '__main__':
    unittest.main()
