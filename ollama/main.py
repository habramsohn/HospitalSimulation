import os
from dotenv import load_dotenv
from input.compile import *
from simulator.run import *

load_dotenv()
api_key = os.getenv('KEY')

if __name__ == "__main__":
    agents = personality_init(personalities, context, api_key)
    run(agents)