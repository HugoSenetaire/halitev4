from agent import *

from kaggle_environments import make

if __name__=="__main__" :
    
    
    # Create a test environment for use later
    board_size = 5
    configuration = {"size": board_size, "startingHalite": 1000}
    environment = make("halite", configuration=configuration)
    agent_count = 2
    environment.reset(agent_count)
    state = environment.state[0]

    actions = base_agent(state.observation, environment.configuration )

