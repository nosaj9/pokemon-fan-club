import requests
from pokeapi.pokemon import Pokemon
import re

class PokeClient(object):
    def __init__(self):
        self.sess = requests.Session()
        self.sess.headers.update({'User Agent': 'CMSC388J Spring 2021 Project 2'})
        self.base_url = 'https://pokeapi.co/api/v2'

    def get_pokemon_list(self):
        """
        Returns a list of pokemon names
        """
        pokemon = []
        resp = self.sess.get(f'{self.base_url}/pokemon?limit=151')
        for poke_dict in resp.json()['results']:
            pokemon.append(poke_dict['name'])
        return pokemon
    
    def get_pokemon_info(self, pokemon):
        """
        Arguments:

        pokemon -- a lowercase string identifying the pokemon

        Returns a dict with info about the Pokemon with the 
        following keys and the type of value they map to:
        
        name      -> string
        height    -> int
        weight    -> int
        base_exp  -> int
        moves     -> list of strings
        abilities -> list of strings
        """

        req = f'pokemon/{pokemon}'
        resp = self.sess.get(f'{self.base_url}/{req}')

        code = resp.status_code
        if code != 200:
            raise ValueError(f'Request failed with status code: {code} and message: '
                             f'{resp.text}')
        
        resp = resp.json()
        
        result = {}

        result['name'] = resp['name']
        result['types'] = resp['types']
        result['height'] = resp['height']
        result['weight'] = resp['weight']
        result['base_exp'] = resp['base_experience']

        result['dex_number'] = resp['id']
        result['sprite'] = resp['sprites']
        
        result['moves'] = Pokemon(result['name']).getMoves()

        abilities = []
        for ability_dict in resp['abilities']:
            abilities.append(ability_dict['ability']['name'])
        
        result['abilities'] = abilities
        result['stats'] = Pokemon(result['name']).getStats()

        locations = []
        loc_resp = self.sess.get(resp['location_area_encounters'])

        code = loc_resp.status_code
        if code != 200:
            raise ValueError(f'Request failed with status code: {code} and message: '
                             f'{loc_resp.text}')
        
        loc_resp = loc_resp.json()

        for i in range(0, len(loc_resp)):
            if re.search("viridian|kanto|moon|rock-tunnel|power-plant|seafoam", loc_resp[i]['location_area']['name']):
            # if "viridian" in loc_resp[i]['location_area']['name'] or "kanto" in loc_resp[i]['location_area']['name']:
                locations.append(loc_resp[i]['location_area']['name'])

        result['locations'] = locations
        # result['test'] = Pokemon(result['name']).getMoveVersionDetails("tackle")[0]
        return result

    def get_ability_description(self, ability):
        req = f'ability/{ability}'
        resp = self.sess.get(f'{self.base_url}/{req}')

        code = resp.status_code
        if code != 200:
            raise ValueError(f'Request failed with status code: {code} and message: '
                             f'{resp.text}')
        
        # no idea why overgrow returns the german one first
        if ability == "overgrow":
            return 'Strengthens grass moves to inflict 1.5× damage at 1/3 max HP or less.'
        else:
            return resp.json()['effect_entries'][len(resp.json()['effect_entries'])-1]['short_effect']
        


    def get_pokemon_with_ability(self, ability):
        """
        Arguments:

        ability -- a lowercase string identifying an ability

        Returns a list of strings identifying pokemon that have the specified ability
        """
        req = f'ability/{ability}'
        resp = self.sess.get(f'{self.base_url}/{req}')

        code = resp.status_code
        if code != 200:
            raise ValueError(f'Request failed with status code: {code} and message: '
                             f'{resp.text}')
    
        kanto_pokemon = []
        resp1 = self.sess.get(f'{self.base_url}/pokemon?limit=151')
        for poke_dict in resp1.json()['results']:
            kanto_pokemon.append(poke_dict['name'])

        pokemon = []
        for poke_dict in resp.json()['pokemon']:
            if poke_dict['pokemon']['name'] in kanto_pokemon:
                pokemon.append(poke_dict['pokemon']['name'])

        return pokemon

## -- Example usage -- ###
if __name__=='__main__':
    client = PokeClient()
    l = client.get_pokemon_list()
    print(len(l))
    print(l[1])

    i = client.get_pokemon_info(l[1])
    print(i.keys())
    print(i['name'])
    print(i['base_exp'])
    print(i['weight'])
    print(i['height'])
    print(i['abilities'])
    print(len(i['moves']))


    p = client.get_pokemon_with_ability('tinted-lens')
    print(p)
