import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
params_path = os.path.join(current_dir, 'parameters.json')

with open(params_path, 'r') as f:
    data = json.load(f)

context = data['sim']['context']
personalities = data['sim']['personalities']
names = list(personalities.keys())
