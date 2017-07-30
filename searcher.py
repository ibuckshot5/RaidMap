import config
import pgoapi
import random
import webhook

from models import Raid

from threading import Thread
from time import sleep
from pgoapi.utilities import f2i, get_cell_ids

def gym_scanner_thread(options):
    id = options.get('id', '')
    lat = options.get('lat', 0)
    lng = options.get('lng', 0)

    sleep(random.randint(0, config.SCAN_BUFFER))

    api = pgoapi.PGoApi()
    api.activate_hash_server(config.HASH_KEY)
    api.set_position(lat, lng, 0)

    api.set_authentication(
        provider='ptc',
        username=options['username'],
        password=options['password'],
        timeout=15
    )

    print('{} logged in.'.format(options['username']))

    req = api.create_request()
    req.get_map_objects(lat=f2i(lat), lng=f2i(lng),
                        since_timestamp_ms=[0, ] * len(get_cell_ids(lat, lng)),
                        cell_id=get_cell_ids(lat, lng))
    req.check_challenge()
    req.get_hatched_eggs()
    req.get_inventory()
    req.check_awarded_badges()
    req.get_buddy_walked()
    req.get_inbox(is_history=True)
    res = req.call()

    gmo = res['responses']['GET_MAP_OBJECTS']

    print('Scanning gym {}...'.format(id))
    # TODO: this is a really bad way to do this
    for cell in gmo.get('map_cells'):
        for fort in cell.get('forts'):
            if fort.get('id') == id:
                if fort.get('raid_info') is not None or fort.get('raid_info') != {}:
                    raid = fort.get('raid_info')
                    print('Found a L{} raid at {}.'.format(raid.get('raid_info'), id))
                    if raid.get('raid_pokemon') is not None or raid.get('raid_pokemon') != {}:
                        pokemon = raid.get('raid_pokemon')
                        webhook.send_to_webhook(fort)
                        Raid.insert(
                            level=raid.get('raid_level'),
                            pokemon_id=pokemon.get('pokemon_id'),
                            latitude=fort.get('latitude'),
                            longitude=fort.get('longitude'),
                            fort_id=fort.get('id'),
                            seed=raid.get('raid_seed'),
                            spawn_time=raid.get('raid_spawn_ms'),
                            battle_time=raid.get('raid_battle_ms'),
                            end_time=raid.get('raid_end_ms'),
                            cp=pokemon.get('cp'),
                            move_1=pokemon.get('move_1'),
                            move_2=pokemon.get('move_2'),
                            controlled_by=fort.get('owned_by_team')
                        )
                    else:
                        Raid.insert(
                            level=raid.get('raid_level'),
                            pokemon_id=None,
                            latitude=fort.get('latitude'),
                            longitude=fort.get('longitude'),
                            fort_id=fort.get('id'),
                            seed=raid.get('raid_seed'),
                            spawn_time=raid.get('raid_spawn_ms'),
                            battle_time=raid.get('raid_battle_ms'),
                            end_time=raid.get('raid_end_ms'),
                            cp=None,
                            move_1=None,
                            move_2=None,
                            controlled_by=fort.get('owned_by_team')
                        )

    sleep(config.SCAN_BUFFER * 60)