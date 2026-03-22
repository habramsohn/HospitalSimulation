import asyncio
from simulator.model import Personality

def personality_init(personalities_dict, context, api_key):
    
    agents = {}
    
    for name, p_params in personalities_dict.items():
                
        agent = Personality(api_key=api_key)
        
        # Create self.prompt and self.name in agent object
        agent.promptBuild(
            context=context,
            name=name,
            occupation=p_params.get('occupation'),
            personality=p_params.get('personality'),
            keyQuestions=p_params.get('keyQuestions'),
            trueKnowledge=p_params.get('trueKnowledge'),
            convoLimit=p_params.get('convoLimit')
        )
        
        agents[name] = agent
    
    return agents

async def conversation(agent): 
    print(f"--- Starting conversation with {agent.name} ---")
    while True:
        message = input("message: ") 
        
        if message.upper() == "STOP":
            break
        
        response = await agent.chat(message)
        print(f"{agent.name}: {response}")
        
        if not hasattr(agent, 'session'):
            print(f"--- Conversation with {agent.name} concluded. Score: {agent.score} ---")
            break
            
# Note; replace with a selection function if desired
def run(agents):
    score = 0
    for agent in agents.values():
        asyncio.run(conversation(agent))
        score += agent.score
    return score