from input.ocompile import *
from simulator.orun import *

if __name__ == "__main__":
    agents = personality_init(personalities, context)
    run(agents)
