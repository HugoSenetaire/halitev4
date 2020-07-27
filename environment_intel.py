
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import kaggle_environments.envs.halite.helpers as halite
from typing import *

## Je pense qu'on peut faire heriter nos classes des classes implémentés dans le SDK, comme ca on bénéficie de leur API
## ca pose peut etre des soucis, auquel cas laisse tomber c'est pas grave
## cf : https://github.com/Kaggle/kaggle-environments/blob/master/kaggle_environments/envs/halite/helpers.py#L350

class Unit():
    """ Abstract class for any unit in Halite """
    

    def __init__(self, id, pos, player_id):
        self.id = id # Unique Id during a whole game
        self.pos = pos # pos
        self.player_id = player_id


        self.is_alive = True
        self.objective = None

    def _actualise(self, is_alive):
        self.is_alive = is_alive

    def _set_objective(self, objective):
        raise NotImplementedError

    def get_available_action(self):
        raise NotImplementedError




class Ship(halite.Ship):
    def __init__(self, *args) -> None:
        super(Ship, self).__init__(*args)

        # self.mothershipyard = mothershipyard
            
        self.halite_cargo = 0
        self.stolen_halite = 0
        self.collected_halite = 0
        self.dropped_halite = 0



    def _actualise(self,
        is_alive = True,
        add_halite_cargo = 0,
        add_stolen_halite = 0,
        add_collected_halite = 0,
        add_dropped_halite = 0
        ):
        """ Actualisation of all the parameters (called by Board) """

        super(Ship, self)._actualise(is_alive = is_alive)

        self.halite_cargo += add_halite_cargo
        self.stolen_halite += add_stolen_halite
        self.stored_halite += add_stored_halite
        self.dropped_halite += add_dropped_halite
    

class Shipyard(halite.Shipyard):
    # Is mothership_id usefull, is it not contained in the shipyard.player_id from the base class ?
    # Or is it another info we want to store here ?
    def __init__(self, *args, mothership_id=None):
        super(Shipyard, self).__init__(*args)
        self.mothership_id = mothership_id

        self.generated_ships = 0
        self.stored_halite = 0


    def _actualise(self,
        is_alive=False, 
        add_generated_ships=0, 
        add_stored_halite=0
        ):
        """ Actualisation of all the parameters (called by Board) """
        super(Shipyard, self)._actualise(is_alive = is_alive)

        self.generated_ships += add_generated_ships
        self.stored_halite += add_stored_halite


class Board(halite.Board):
    def __init__(self, obs, config):
        self.map_to_ship = {} #For each player, ship_id
        super(Board, self).__init__(obs,config)
        # self.current_player =


    def check_actualisation(self, obs):
        """ Actualisation is made without the observation. Make sure everything works"""
        raise NotImplementedError
        
    def actualise(self, obs, config, actions):
        # Need to get which move was played by the opponents 
        raise NotImplementedError
    
    # We override the basic _add_ship methods called in the constructor of the halite.Board class so that the ships are instances of our custom Ship class (instead of the halite.Ship class)
    # Need to make sure that the constructor of the base class actually calls this method instead of the base method (not sure about that)
    def _add_ship(self: 'Board', ship: halite.Ship) -> None:
        ship.player.ship_ids.append(ship.id)
        ship.cell._ship_id = ship.id
        self._ships[ship.id] = Ship(ship.id, ship.position, ship.halite, ship.player_id, self) #We create a Ship instance from our custom class
    
    # Same thing applies for _add_shipyard
    def _add_shipyard(self: 'Board', shipyard: halite.Shipyard) -> None:
        shipyard.player.shipyard_ids.append(shipyard.id)
        shipyard.cell._shipyard_id = shipyard.id
        shipyard.cell._halite = 0
        self._shipyards[shipyard.id] = Shipyard(shipyard.id, shipyard.position, shipyard.player_id, self)

        

def get_map_and_average_halite(obs):
    """
        get average amount of halite per halite source
        and map as two dimensional array of objects and set amounts of halite in each cell
    """
    game_map = []
    halite_sources_amount = 0
    halite_total_amount = 0
    for x in range(conf.size):
        game_map.append([])
        for y in range(conf.size):
            game_map[x].append({
                # value will be ID of owner
                "shipyard": None,
                # value will be ID of owner
                "ship": None,
                # value will be amount of halite
                "ship_cargo": None,
                # amount of halite
                "halite": obs.halite[conf.size * y + x]
            })
            if game_map[x][y]["halite"] > 0:
                halite_total_amount += game_map[x][y]["halite"]
                halite_sources_amount += 1
    average_halite = halite_total_amount / halite_sources_amount
    return game_map, average_halite

def get_swarm_units_coords_and_update_map(s_env):
    """ get lists of coords of Swarm's units and update locations of ships and shipyards on the map """
    # arrays of (x, y) coords
    swarm_shipyards_coords = []
    swarm_ships_coords = []
    # place on the map locations of units of every player
    for player in range(len(s_env["obs"].players)):
        # place on the map locations of every shipyard of the player
        shipyards = list(s_env["obs"].players[player][1].values())
        for shipyard in shipyards:
            x = shipyard % conf.size
            y = shipyard // conf.size
            # place shipyard on the map
            s_env["map"][x][y]["shipyard"] = player
            if player == s_env["obs"].player:
                swarm_shipyards_coords.append((x, y))
        # place on the map locations of every ship of the player
        ships = list(s_env["obs"].players[player][2].values())
        for ship in ships:
            x = ship[0] % conf.size
            y = ship[0] // conf.size
            # place ship on the map
            s_env["map"][x][y]["ship"] = player
            s_env["map"][x][y]["ship_cargo"] = ship[1]
            if player == s_env["obs"].player:
                swarm_ships_coords.append((x, y))
    return swarm_shipyards_coords, swarm_ships_coords

def to_spawn_or_not_to_spawn(s_env):
    """ to spawn, or not to spawn, that is the question """
    # get ships_max_amount to decide whether to spawn new ships or not
    ships_max_amount = 9
    # if ships_max_amount is less than minimal allowed amount of ships in the Swarm
    if ships_max_amount < ships_min_amount or s_env["obs"].step >= spawn_stop_step:
        ships_max_amount = ships_min_amount
    return ships_max_amount

def get_intel(observation, s_env):
    """ Transform intel to classic vector transformation """
    shipyards_map = {}
    ships_map = {}
    ships_cargo_map = {}
    for player in range(len(s_env["obs"].players)):
        # Shipyard maps :
        shipyards_map[player] = np.zeros(conf.size*conf.size)
        shipyards = list(s_env["obs"].players[player][1].values())
        for shipyard in shipyards:
            shipyards_map[player][shipyard] = 1
        # Get ships map :
        ships_map[player] = np.zeros(conf.size*conf.size)
        ships_cargo_map[player] = np.zeros(conf.size*conf.size)
        ships = list(s_env["obs"].players[player][2].values())
        for ship in ships:
            #x = ship[0] % conf.size
            #y = ship[0] // conf.size
            ships_map[player][ship[0]]=1
            ships_cargo_map[player][ship[0]] = ship[1]
            
    return shipyards_map,ships_map,ships_cargo_map
 
           
    
def adapt_environment(observation, configuration):
    """ adapt environment for the Swarm """
    s_env = {}
    s_env["obs"] = observation
    if globals_not_defined:
        define_some_globals(configuration)
    s_env["map"], s_env["average_halite"] = get_map_and_average_halite(s_env["obs"])
    s_env["low_amount_of_halite"] = s_env["average_halite"] * 0.75
    s_env["swarm_halite"] = s_env["obs"].players[s_env["obs"].player][0]
    s_env["swarm_shipyards_coords"], s_env["swarm_ships_coords"] = get_swarm_units_coords_and_update_map(s_env)
    s_env["ships_keys"] = list(s_env["obs"].players[s_env["obs"].player][2].keys())
    s_env["ships_values"] = list(s_env["obs"].players[s_env["obs"].player][2].values())
    s_env["shipyards_keys"] = list(s_env["obs"].players[s_env["obs"].player][1].keys())
    s_env["ships_max_amount"] = to_spawn_or_not_to_spawn(s_env)
    s_env["shipyards_map"],s_env["ships_map"],s_env["ships_cargo_map"] = get_intel(s_env["obs"],s_env)
    return s_env
