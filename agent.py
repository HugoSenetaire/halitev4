from environment_intel import *
from random import choice
import kaggle_environments.envs.halite.helpers as halite


def swarm_agent(observation, configuration):
    """ RELEASE THE SWARM!!! """
    s_env = adapt_environment(observation, configuration)
    actions = actions_of_ships(s_env)
    actions = actions_of_shipyards(actions, s_env)
    return actions

def base_agent(observation, configuration):
    board = Board(observation,configuration)
    me = board.current_player

    # Set actions for each ship
    for ship in me.ships:
        # We check whether the ships are from our custom class
        print(type(ship))
        #We can call custom methods
        ship.custom_method()
        #The SDK methods also class because our custom class inherits from it
        ship.next_action = choice([halite.ShipAction.NORTH,halite.ShipAction.EAST,halite.ShipAction.SOUTH,halite.ShipAction.WEST,None])

    # Set actions for each shipyard
    for shipyard in me.shipyards:
        shipyard.next_action = None

    return me.next_actions
