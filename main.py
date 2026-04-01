import os
from dotenv import load_dotenv
from compile import *
import gemini as g
from gemini import main

load_dotenv()
api_key = os.getenv('KEY')

if __name__ == "__main__":
    agents = g.main.personality_init(personalities, context, api_key)
    g.main.run(agents)
