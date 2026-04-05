import asyncio
from .model import Agent

def personality_init(personalities_dict, context, api_key):
    
    agents = {}
    
    for name, p_params in personalities_dict.items():
                
        agent = Agent(api_key=api_key)
        
        # Create self.prompt and self.name in agent object
        agent.promptBuild(
            context=context,
            name=name,
            occupation=p_params.get('occupation'),
            personality=p_params.get('personality'),
            knowledge=p_params.get('knowledge'),
            bias=p_params.get('bias'),
            triggers=p_params.get('triggers'),
            constrained=p_params.get('constrained'),
            convoLimit=p_params.get('convoLimit')
        )
        
        agents[name] = agent
    
    return agents

def conversation(agent, message): 
    response = agent.chat(message)
    return response
            
def run(agent, message):
    return conversation(agent, message)