import csv

from peewee import OperationalError

from exceptions import NotEnoughRecordsError
from models import Passenger


def on_startup():
    try:
        _checking_if_records_exist_in_the_database()
    except OperationalError:
        _create_tables()
        on_startup()
    except NotEnoughRecordsError:
        _convert_from_csv_to_sqlite()


def _checking_if_records_exist_in_the_database():
    csv_rows_count = _get_csv_rows_count()
    try:
        db_recors_count = _get_db_records_count()
    except OperationalError:
        raise OperationalError
    
    if csv_rows_count == db_recors_count:
        return
    raise NotEnoughRecordsError()


def _get_csv_rows_count():
    with open('titanic.csv') as csvf:
        reader = csv.reader(csvf)
        return len(list(reader)) - 1


def _get_db_records_count():
    try:
        return Passenger.select().count()
    except OperationalError:
        raise OperationalError


def _create_tables():
    Passenger.create_table()


def _convert_from_csv_to_sqlite():
    with open('titanic.csv') as csvf:
        reader = csv.DictReader(csvf)
        for row in reader:
            fields = dict((k.lower(), v) for k, v in row.items())
            fields['id'] = fields.pop('passengerid')
            fields['age'] = None if fields['age'] == '' else fields['age']
            fields['cabin'] = None if fields['cabin'] == '' else fields['cabin']
            fields['embarked'] = None if fields['embarked'] == '' else fields['embarked']
            Passenger.create(**fields)


def get_top_10_passengers():
    passengers = Passenger.select().where(Passenger.age>=18, Passenger.age!=None)\
            .order_by(Passenger.age.asc()).limit(10).dicts()
    return list(p for p in passengers)


def get_all_passenger():
    passengers = Passenger.select().dicts()
    return list(p for p in passengers)
