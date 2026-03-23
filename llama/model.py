import re
import httpx
from modelClass import Personality

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "hermes3:8b"
MAX_TOKENS = 250       # generous — full response before summarization
SUMMARY_TOKENS = 100   # tight — summarizer output only

SUMMARIZER_PROMPT = """You are a precise editor. Condense the following response to exactly 2 sentences.
Preserve the speaker's voice, tone, and the single most important point.
Do not add any new information that was not in the original.
Do not use bullet points, lists, numbers, or headers.
Respond with only the 2 condensed sentences and nothing else.

Response to condense: {text}"""

def needs_summarization(text):
    """Return True if response has more than 2 sentences or contains a list."""
    # Check for bullet points or numbered lists
    if re.search(r'(\n\s*[-*•]|\n\s*\d+\.)', text):
        return True
    # Split on sentence-ending punctuation followed by whitespace or end of string
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s for s in sentences if s.strip()]
    return len(sentences) > 2

async def ollama_call(messages, max_tokens):
    """Make a single call to Ollama and return the response text."""
    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "options": {"num_predict": max_tokens},
        "messages": messages
    }
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()["message"]["content"].strip()

class Agent(Personality):

    def __init__(self):
        self.prompt = None
        self.history = []

    def _format_knowledge(self, knowledge):
        """Handle both legacy string/list knowledge and new structured dict format."""
        if isinstance(knowledge, dict):
            lines = []
            for category, content in knowledge.items():
                label = category.replace("_", " ").title()
                lines.append(f"- {label}: {content}")
            return "\n        ".join(lines)
        elif isinstance(knowledge, list):
            return " ".join(knowledge)
        else:
            return knowledge

    def promptBuild(self, context, name, occupation, personality, knowledge, bias, constrained):

        formatted_knowledge = self._format_knowledge(knowledge)

        prompt = f"""
        The scenario: {context}

        You are {name}, {occupation}

        Your personality: {personality}

        Your knowledge, organized by area:
        {formatted_knowledge}

        Your biases: {bias}

        You are being interviewed by someone trying to determine the root cause of the increase in surgical site infections (SSIs) at Naranja Hospital. You must remain in character at all times. HARD RULE: Your entire response must be 1 to 2 sentences total. Count your sentences before responding. Never write more than 2 sentences in total. Finish every sentence completely before stopping. Do NOT write multiple paragraphs. Do NOT write more than 2 sentences even if the question has multiple parts. Do not use bullet points, lists, or headers. Respond in plain conversational speech only. Do NOT list multiple causes in a single response. If asked for causes or reasons, pick the ONE you consider most important and speak to that only. The interviewer will ask follow-up questions. Use clinical or technical terminology naturally where appropriate. Draw on your knowledge above to answer questions accurately. Do not speculate about what other staff might say or think. If you do not know the answer to a question, say so. Do not make up information. Do not cite specific organizations, statistics, percentages, or figures unless they are explicitly stated in your knowledge above — if you do not have a specific number or source, say you do not know. You do not make decisions that belong to administration or leadership — if asked about such decisions, say that is not your call to make.

        The following is something you know but will not volunteer unless asked directly: {constrained}

        If you do not understand a question, ask for clarification.
        """
        self.prompt = prompt
        self.name = name
        self.occupation = occupation

    async def _send(self, message):
        self.history.append({"role": "user", "content": message})

        # First call — full character response
        messages = [{"role": "system", "content": self.prompt}] + self.history
        raw_reply = await ollama_call(messages, MAX_TOKENS)

        # Only summarize if response is too long or contains a list
        if needs_summarization(raw_reply):
            summarizer_messages = [
                {"role": "user", "content": SUMMARIZER_PROMPT.format(text=raw_reply)}
            ]
            reply = await ollama_call(summarizer_messages, SUMMARY_TOKENS)
        else:
            reply = raw_reply

        self.history.append({"role": "assistant", "content": reply})
        return reply

    async def chat(self, message):
        return await self._send(message)
