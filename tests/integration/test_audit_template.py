import unittest

from mongoengine import connect

from cilantro_audit.audit_template import AuditTemplate, AuditTemplateBuilder, Question, Severity
from cilantro_audit.constants import TEST_DB

connect(TEST_DB)


class AuditTemplateTests(unittest.TestCase):

    def __del__(self):
        db = connect(TEST_DB)
        db.drop_database(TEST_DB)

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

        template = templates[0]

        self.assertEqual(q0_text, template.questions[0].text)
        self.assertEqual(Severity.green(), template.questions[0].yes)
        self.assertEqual(Severity.green(), template.questions[0].no)
        self.assertEqual(Severity.green(), template.questions[0].other)

        self.assertEqual(q1_text, template.questions[1].text)
        self.assertEqual(Severity.red(), template.questions[1].yes)
        self.assertEqual(Severity.green(), template.questions[1].no)
        self.assertEqual(Severity.green(), template.questions[1].other)

        self.assertEqual(q2_text, template.questions[2].text)
        self.assertEqual(Severity.green(), template.questions[2].yes)
        self.assertEqual(Severity.red(), template.questions[2].no)
        self.assertEqual(Severity.yellow(), template.questions[2].other)
