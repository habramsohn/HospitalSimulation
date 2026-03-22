import os
from dotenv import load_dotenv
from compile import *
import gemini as g
from gemini import main
import ollama as o
from ollama import main

load_dotenv()
api_key = os.getenv('KEY')

choice = input("Select a model: \n 1 - Gemini \n 2 - Ollama \n")

if __name__ == "__main__":
    if choice == "1":
        agents = g.main.personality_init(personalities, context, api_key)
        g.main.run(agents)
    elif choice == "2": 
        agents = o.personality_init(personalities, context)
        o.main.run(agents)