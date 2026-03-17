import asyncio
import google.genai as genai

class Personality:
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.score = 0
        self.prompt = None

    def promptBuild(self, context, name, occupation, personality, keyQuestions, trueKnowledge, falseKnowledge, convoLimit):
        prompt = f"""
        The scenario: {context}
        
        You are {name}, {occupation}
        
        Your personality is: {personality}
        
        You are being interviewed. You may only act in character. 
        
        KEYS: If you are asked one of the following: {keyQuestions}, respond with the most relevant from the following: {trueKnowledge}
        
        WRONGS: If you are asked an irrelevant, rude, or otherwise insufficient question, respond with the most relevant from the following: {falseKnowledge}
        
        If you do not understand a question, you may ask to clarify it. 
        
        You may return up to {convoLimit} substantive answers. After this limit, leave. 
        
        HARD RULE: After excusing yourself, you may send this and nothing else: "DONE"  

        HARD RULE: Only after you receive the following prompt - "EXIT" - do this:
        
        Report each of the following data as a single integer in the specified format:
        
        KEYS|WRONGS
        """
        self.name = name
        self.prompt = prompt
    
    async def chat(self, message):
        if not hasattr(self, 'session'):
            self.session = self.client.aio.chats.create(
                model="gemini-3-flash-preview",
                config={'system_instruction': self.prompt}
            )

        response = await self.session.send_message(message)
    
        if response.text == "DONE":
            print("done")
            response = await self.session.send_message("EXIT")
            right = int(response.text.split("|")[0])
            wrong = int(response.text.split("|")[1])
            self.score = right - wrong
        
        return response.text