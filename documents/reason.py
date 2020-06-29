from mongoengine import Document, StringField, ReferenceField, DateTimeField

from documents.user import User


class Reason(Document):
    # TODO In mysql I would set the date, owner and target as primary key, doesn't work here?
    date = DateTimeField(required=True)
    # owner = ReferenceField(User, primary_key=True)
    # target = ReferenceField(User, primary_key=True)
    owner = ReferenceField(User)
    target = ReferenceField(User)
    reason = StringField(required=True)
