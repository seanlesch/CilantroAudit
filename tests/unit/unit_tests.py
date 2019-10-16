from test_severity import SeverityTests
from test_question import QuestionTests
from test_audit_template import AuditTemplateTests
from test_audit_template_builder import AuditTemplateBuilderTests



if __name__ == '__main__':
    SeverityTests.run_tests()
    QuestionTests.run_tests()
    AuditTemplateTests.run_tests()
    AuditTemplateBuilderTests.run_tests()
