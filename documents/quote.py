from mongoengine import Document, StringField, ReferenceField, DateTimeField

from documents.user import User


class Quote(Document):
    date = DateTimeField(required=True)
    quotee = ReferenceField(User)
    quoter = ReferenceField(User)
    quote = StringField(required=True)
