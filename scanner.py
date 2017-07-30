import config
import sys
import searcher
import random

from multiprocessing import Pool
from peewee import MySQLDatabase

def main():
    SCANNERS = []
    with open(config.ACCOUNTS_FILE, 'r') as f:
        for num, line in enumerate(f, 1):
            fields = line.split(",")
            fields = map(str.strip, fields)
            SCANNERS.append({'username': fields[0], 'password': fields[1]})

    gyms = get_gyms()

    if len(gyms) == 0:
        print('Found 0 gyms in queue. Please add more.')
        sys.exit(1)
    else:
        print('Found {} gyms in queue.'.format(len(gyms)))

    p = Pool()

    xyl = []
    ranscan = random.choice(SCANNERS)
    for gym in gyms:
        xyl.append({
            'id': gym.get('id'),
            'lat': gym.get('lat'),
            'lng': gym.get('lng'),
            'username': ranscan['username'],
            'password': ranscan['password']
        })



    p.map(searcher.gym_scanner_thread, xyl)

def get_gyms():
    gyms = []
    database = MySQLDatabase(database=config.BASE_DB['database'], user=config.BASE_DB['username'],
                       password=config.BASE_DB['password'], host=config.BASE_DB['host'])
    if config.BASE_DB_TYPE == 0:
        cursor = database.execute_sql('SELECT * FROM gyms;')
        for row in cursor.fetchall():
            gyms.append({
                'id': str(row['gym_id']),
                'lat': row['latitude'],
                'lng': row['longitude']
            })
    elif config.BASE_DB_TYPE == 1:
        cursor = database.execute_sql('SELECT * FROM forts;')
        for row in cursor.fetchall():
            gyms.append({
                'id': str(row[1]),
                'lat': float(row[2]),
                'lng': float(row[3])
            })

    return gyms

if __name__ == '__main__':
    main()