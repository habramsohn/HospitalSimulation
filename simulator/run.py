import asyncio
from simulator.model import Personality

def personality_init(personalities_dict, context, api_key):
    
    agents = {}
    
    for p_id, p_params in personalities_dict.items():
                
        agent = Personality(api_key=api_key)
        
        agent.promptBuild(
            context=context,
            name=p_params.get('name'),
            occupation=p_params.get('occupation'),
            personality=p_params.get('personality'),
            keyQuestions=p_params.get('keyQuestions'),
            trueKnowledge=p_params.get('trueKnowledge'),
            falseKnowledge=p_params.get('falseKnowledge'),
            convoLimit=p_params.get('convoLimit')
        )
        
        agents[p_id] = agent
    
    return agents

async def conversation(agent): 
    fin = False
    
    while fin == False:
        message = input("message: ") 
        response = await agent.chat(message)
        print(f"{agent.name}: {response}")
    
        if message == "STOP" or "DONE" in response:
            fin = True
            
def run(agents):
    for agent in agents.values():
        asyncio.run(conversation(agent))