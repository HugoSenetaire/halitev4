from environment_intel import *



def swarm_agent(observation, configuration):
    """ RELEASE THE SWARM!!! """
    s_env = adapt_environment(observation, configuration)
    actions = actions_of_ships(s_env)
    actions = actions_of_shipyards(actions, s_env)
    return actions