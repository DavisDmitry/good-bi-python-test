from peewee import (AutoField, BooleanField, CharField, IntegerField,
                    FloatField, Model, SqliteDatabase)


db = SqliteDatabase('titanic.db')


class BaseModel(Model):
    class Meta:
        database = db


class Passenger(BaseModel):
    id = AutoField(primary_key=True)
    survived = BooleanField()
    pclass = IntegerField()
    name = CharField(max_length=90)
    sex = BooleanField()
    age = IntegerField(null=True)
    sibsp = IntegerField()
    parch = IntegerField()
    ticket = CharField(max_length=20)
    fare = FloatField()
    cabin = CharField(max_length=20, null=True)
    embarked = CharField(max_length=1, null=True)

    class Meta:
        table_name = 'passengers'
