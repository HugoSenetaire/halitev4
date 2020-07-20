from agent import *

from kaggle_environments import make
from kaggle_environments.envs.halite.helpers import *

if __name__=="__main__" :
    
    
    # Create a test environment for use later
    board_size = 5
    environment = make("halite", configuration={"size": board_size, "startingHalite": 1000})
    agent_count = 2
    environment.reset(agent_count)
    state = environment.state[0]