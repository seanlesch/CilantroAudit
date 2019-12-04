import hashlib
from _hashlib import HASH

from mongoengine import connect, Document, StringField

from cilantro_audit.constants import PROD_DB

connect(PROD_DB)


class PasswordHash(Document):
    value = StringField(required=True)


def sha512_encode(s):
    return hashlib.sha512(s.encode('utf-8')).hexdigest()


def password_is_valid(password):
    actual = sha512_encode(password)
    expected = PasswordHash.objects[0].value
    return actual == expected


def update_password(password):
    PasswordHash.objects.delete()
    PasswordHash(sha512_encode(password)).save()
