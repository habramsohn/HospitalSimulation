import httpx
from modelClass import Personality

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "hermes3:8b"

class Agent(Personality):
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=120.0)

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
