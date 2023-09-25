from peewee import Model, IntegerField, TextField
from database import db

class Ayah(Model):
    id = IntegerField(primary_key=True)
    surah_id = IntegerField()
    ayah = IntegerField()
    page = IntegerField()
    quarter_hizb = IntegerField()
    juz = IntegerField()
    manzil = IntegerField()
    arabic = TextField()
    kitabah = TextField()
    latin = TextField()
    translation = TextField()
    footnotes = TextField()

    class Meta:
        database = db
        table_name = 'ayah'
