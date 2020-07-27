from agent import *

from kaggle_environments import make

if __name__=="__main__" :
    
    
    # # Create a test environment for use later
    board_size = 15
    configuration = {"size": board_size, "startingHalite": 1000}

    from kaggle_environments import make
    env = make("halite", debug=True, configuration=configuration)
    env.run(["agent.py", "agent.py", "agent.py", "random"])
    out = env.render(mode="html",width=800, height=600)
    with open('halite.html', 'w') as f:
        f.write(out)
        f.close()



