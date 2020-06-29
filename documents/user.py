from mongoengine import Document, IntField, StringField


class User(Document):
    id = IntField(primary_key=True, required=True)
    name = StringField(required=True)
    warnings = IntField(required=True, default=0)
