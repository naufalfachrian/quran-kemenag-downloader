from peewee import Model, IntegerField, TextField
from database import db


class Surah(Model):
    id = IntegerField(primary_key=True)
    arabic = TextField()
    latin = TextField()
    transliteration = TextField()
    translation = TextField()
    num_ayah = IntegerField()
    page = IntegerField()
    location = TextField()

    class Meta:
        database = db
        table_name = 'surah'
