import asyncio
from ollama.simulator.model import Personality

def personality_init(personalities_dict, context):
    
    agents = {}
    
    for name, p_params in personalities_dict.items():
                
        agent = Personality()
        
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

async def conversation(agent): 
    print(f"--- Starting conversation with {agent.name} ---")
    while True:
        message = input("message: ") 
        
        if message.upper() == "STOP":
            break
        
        response = await agent.chat(message)
        print(f"{agent.name}: {response}")
        
        if not agent.history:
            print(f"--- Conversation with {agent.name} concluded. Score: {agent.score} ---")
            break
            
def select_agent(agents):
    names = list(agents.keys())
    print("\n--- Select an agent to interview ---")
    for i, (name, agent) in enumerate(agents.items(), 1):
        occupation = ', '.join(agent.occupation) if isinstance(agent.occupation, list) else agent.occupation
        print(f"  {i}. {name} — {occupation}")
    while True:
        choice = input("Enter number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(names):
            return agents[names[int(choice) - 1]]
        print(f"  Please enter a number between 1 and {len(names)}.")

def run(agents):
    score = 0
    while True:
        agent = select_agent(agents)
        asyncio.run(conversation(agent))
        score += agent.score
        again = input("\nInterview another agent? (y/n): ").strip().lower()
        if again != 'y':
            break
    print(f"\n=== Session complete. Total score: {score} ===")
    return score