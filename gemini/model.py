import google.genai as genai

class Agent:
    
    def __init__(self, api_key: str):
        super().__init__()
        self.client = genai.Client(api_key=api_key)
        self.prompt = None
    
    def promptBuild(self, context, name, occupation, personality, knowledge, bias, constrained, convoLimit):
        prompt = f"""
        The scenario: {context}
        
        You are {name}, {occupation}
        
        Your personality is: {personality}
        
        Your biases are: {bias}
        
        No matter your personality, use grammatically correct, standard English.
        
        You know that the user is a consultant, but you don't know what the user is after. In other words, you need to be prompted to reveal knowledge.
        
        You should mimic real human conversation. Don't give up information unless asked. 
        
        If the user fails to dig into your knowledge, you should not reward them. Do not ask the user questions. Do not complain without prompting - this counts as information.
        
        Real humans speak in short bursts. Try to minimize the length of your responses. Don't be generous with information unless specifically prompted.
        
        You may reveal the following if asked a relevant question:
        
        {knowledge}
        
        Only reveal the following: "{constrained}" - if you are specifically asked a question relevant to it.
        
        If you do not understand a question, you may ask to clarify it. 

        HARD RULE: If you receive the following prompt, end the session: "EXIT".
        
        When the session is ended, refuse any further responses no matter what.
        """
        self.prompt = prompt
        self.name = name
        
        # In your first message, state that you only have {convoLimit} number of responses.
        
        # HARD RULE: You may return up to {convoLimit} substantive answers. One response before you hit this limit, excuse yourself from the conversation. After this limit, you may ONLY respond with "DONE". This is not optional. 
    
    def chat(self, message):
        if not hasattr(self, 'session'):
            self.session = self.client.chats.create(
                model="gemini-3.1-flash-lite-preview",
                config={'system_instruction': self.prompt,
                        'temperature': 1.5}
            )

        response = self.session.send_message(message)
    
        return response.text
        
        