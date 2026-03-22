import asyncio
import google.genai as genai
from modelClass import Personality

class Agent(Personality):
    
    def __init__(self, api_key: str):
        super().__init__()
        self.client = genai.Client(api_key=api_key)
        self.prompt = None
    
    async def chat(self, message):
        if not hasattr(self, 'session'):
            self.session = self.client.aio.chats.create(
                model="gemini-3-flash-preview",
                config={'system_instruction': self.prompt}
            )

        response = await self.session.send_message(message)
    
        if response.text == "DONE":
            print("admin note: done")
            response = await self.session.send_message("EXIT")
            right = int(response.text.split("|")[0])
            wrong = int(response.text.split("|")[1])
            self.score = right - wrong
            del self.session
        
        return response.text