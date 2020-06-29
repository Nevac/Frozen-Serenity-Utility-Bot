from mongoengine import Document, StringField, ReferenceField, DateTimeField

from documents.user import User


class Warnig(Document):
    date = DateTimeField(required=True)
    owner = ReferenceField(User)
    target = ReferenceField(User)
    reason = StringField(required=True)
