import httpx

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "hermes3:8b"

class Personality:
    
    def __init__(self):
        self.score = 0
        self.prompt = None
        self.history = []
        # Persistent client avoids Windows asyncio cancellation issues
        self.client = httpx.AsyncClient(timeout=120.0)

    def promptBuild(self, context, name, occupation, personality, knowledge, bias, triggers, constrained, convoLimit):
        prompt = f"""
        The scenario: {context}
        
        You are {name}, {occupation}
        
        Your personality is: {personality}

        Your baseline knowledge is: {knowledge}
        
        Your biases are: {bias}
        
        You are being interviewed by someone who is trying to determine the root cause of the increase in surgical site infections (SSIs) at Naranja Hospital. You must remain in character. You may respond with up to 4 sentences, but prefer shorter. Use technical terminology when appropriate.  Rely on your {knowledge} as much as possible to answer questions. Do not speculate about what other staff might say or think. If you do not know the answer to a question, say you do not know. Do not make up information. Do not bring up information related to {constrained} unless asked about it directly or a {triggers} is asked.
        
        KEYS: If you are asked one of the following: {triggers}, respond with the most relevant from the following: {constrained}
        
        If you do not understand a question, you may ask to clarify it. 
        
        HARD RULE: You may return up to {convoLimit} substantive answers. After this limit, you must leave. This is not optional. 
        
        HARD RULE: After excusing yourself, your next prompt must contain this and nothing else: "DONE"  

        HARD RULE: Only after you receive the following prompt - "EXIT" - do this:
        
        Report each of the following data as a single integer in the specified format:
        
        KEYS|NONKEYS
        """
        self.prompt = prompt
        self.name = name
        self.occupation = occupation

    async def _send(self, message):
        """Append message to history, send full history to Ollama, return reply text."""
        self.history.append({"role": "user", "content": message})

        payload = {
            "model": OLLAMA_MODEL,
            "stream": False,
            "messages": [{"role": "system", "content": self.prompt}] + self.history
        }

        response = await self.client.post(OLLAMA_URL, json=payload)
        response.raise_for_status()

        reply = response.json()["message"]["content"].strip()
        self.history.append({"role": "assistant", "content": reply})
        return reply

    async def chat(self, message):
        response_text = await self._send(message)

        if response_text.strip() == "DONE":
            print("admin note: done")
            exit_text = await self._send("EXIT")
            try:
                parts = exit_text.strip().split("|")
                right = int(parts[0])
                wrong = int(parts[1])
                self.score = right - wrong
            except (ValueError, IndexError):
                print(f"admin note: could not parse score from: '{exit_text}'")
                self.score = 0
            await self.client.aclose()
            self.history = []

        return response_text
