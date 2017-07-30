import config
import time
import base64
import requests

def send_to_webhook(fort):
    raid = fort.raid_info
    pokemon = raid.raid_pokemon
    json = {
        'type': 'pokemon',
        'message': {
            'disappear_time': raid.raid_end_ms,
            'form': None,
            'seconds_until_despawn': calc_seconds_to_despawn(raid.raid_end_ms),
            'spawnpoint_id': 'idk',
            'cp_multiplier': pokemon.cp_multiplier,
            'move_2': pokemon.move_2,
            'height': None,
            'time_until_hidden_ms': raid.raid_end_ms, # wtf
            'last_modified_time': int(round(time.time() * 1000)), # idk what to put here
            'cp': pokemon.cp,
            'encounter_id': base64.b64encode(str(raid.raid_level).encode()),
            'spawn_end': 0,
            'move_1': pokemon.move_1,
            'individual_defense': pokemon.individual_defense,
            'verified': True, # we LITERALLY just found it robert
            'weight': None,
            'pokemon_id': pokemon.pokemon_id,
            'player_level': 5, # idk also
            'individual_stamina': pokemon.individual_stamina,
            'longitude': fort.longitude,
            'spawn_start': 0,
            'pokemon_level': None,
            'gender': pokemon.pokemon_display.gender,
            'latitude': fort.latitude,
            'individual_attack': pokemon.individual_attack
        }
    }

    for webook in config.WEBHOOKS:
        requests.post(webook, data=json)

def calc_seconds_to_despawn(raid_end):
    current = int(round(time.time() * 1000))
    yes = raid_end - current
    return yes / 1000

