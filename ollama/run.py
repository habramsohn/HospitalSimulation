import asyncio
from simulator.model import Personality

def personality_init(personalities_dict, context):

    agents = {}

    for name, p_params in personalities_dict.items():

        agent = Personality()

        agent.promptBuild(
            context=context,
            name=name,
            occupation=p_params.get('occupation'),
            personality=p_params.get('personality'),
            knowledge=p_params.get('knowledge'),
            bias=p_params.get('bias'),
            constrained=p_params.get('constrained')
        )

        agents[name] = agent

    return agents

async def conversation(agent):
    print(f"\n--- Starting conversation with {agent.name} ---")
    print("(type STOP to end the conversation)\n")
    while True:
        message = input("You: ").strip()

        if message.upper() == "STOP":
            print(f"--- Conversation with {agent.name} ended ---")
            break

        if not message:
            continue

        response = await agent.chat(message)
        print(f"\n{agent.name}: {response}\n")

def select_agent(agents):
    names = list(agents.keys())
    print("\n" + "="*50)
    print("  SELECT AN AGENT TO INTERVIEW")
    print("="*50)
    for i, (name, agent) in enumerate(agents.items(), 1):
        occupation = ', '.join(agent.occupation) if isinstance(agent.occupation, list) else agent.occupation
        print(f"  {i}. {name} — {occupation}")
    print("  Q. Quit")
    print("="*50)
    while True:
        choice = input("Enter number: ").strip().upper()
        if choice == "Q":
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(names):
            return agents[names[int(choice) - 1]]
        print(f"  Please enter a number between 1 and {len(names)}, or Q to quit.")

def run(agents):
    while True:
        agent = select_agent(agents)
        if agent is None:
            break
        asyncio.run(conversation(agent))
        input("\nPress Enter to return to the agent selection menu...")
    print("\n=== Session complete ===")
