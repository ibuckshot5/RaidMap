import config
from peewee import *

db = MySQLDatabase(database=config.DATABASE['database'], user=config.DATABASE['username'], password=config.DATABASE['password'], host=config.DATABASE['host'])

class BaseModel(Model):
    class Meta:
        database = db

class Raid(BaseModel):
    id = IntegerField(primary_key=True)
    level = SmallIntegerField()
    pokemon_id = IntegerField()
    latitude = DoubleField(17, 14)
    longitude = DoubleField(17, 14)
    fort_id = CharField(50)
    seed = BigIntegerField()
    spawn_time = BigIntegerField()
    battle_time = BigIntegerField()
    end_time = BigIntegerField()
    cp = IntegerField()
    move_1 = SmallIntegerField()
    move_2 = SmallIntegerField()
    controlled_by = SmallIntegerField()