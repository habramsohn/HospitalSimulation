from input.compile import *
from simulator.run import *

if __name__ == "__main__":
    agents = personality_init(personalities, context)
    run(agents)
