from mongoengine import Document, StringField, EmbeddedDocument, EmbeddedDocumentField, EmbeddedDocumentListField


class ResponseEnum:
    YES = "YES"
    NO = "NO"
    OTHER = "OTHER"


class Response(EmbeddedDocument):
    response = StringField(required=True)

    @staticmethod
    def yes():
        return Response(ResponseEnum.YES)

    @staticmethod
    def no():
        return Response(ResponseEnum.NO)

    @staticmethod
    def other():
        return Response(ResponseEnum.OTHER)


class Answer(EmbeddedDocument):
    text = StringField(required=True, max_length=50, min_length=1)
    response = EmbeddedDocumentField(Response, required=True)
    comments = StringField(max_length=150, min_length=1)


class CompletedAudit(Document):
    title = StringField(required=True, max_length=50, min_length=1)
    answers = EmbeddedDocumentListField(Answer, required=True)
