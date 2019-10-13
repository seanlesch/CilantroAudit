from source.audit_template import AuditTemplate

class AuditTemplateBuilder:
    def __init__(self):
        self.title = None
        self.questions = []

    def with_title(self, title):
        self.title = title
        return self

    def with_question(self, question):
        self.questions.append(question)
        return self

    def build(self):
        template = AuditTemplate(title=self.title, questions=self.questions)
        template.validate()
        return template
