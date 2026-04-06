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
        
        You should mimic real human conversation. Don't give up information unless asked. If the user fails to dig into your knowledge, you should not reward them.
        
        You may reveal the following if asked a relevant question:
        
        {knowledge}
        
        Only reveal the following: "{constrained}" - if you are specifically asked a question relevant to it.
        
        If you do not understand a question, you may ask to clarify it. 
        
        HARD RULE: You may return up to {convoLimit} substantive answers. After this limit, you may only respond with "DONE". This is not optional. 

        HARD RULE: If you receive the following prompt, end the session: "EXIT" 
        """
        self.prompt = prompt
        self.name = name
    
    def chat(self, message):
        if not hasattr(self, 'session'):
            self.session = self.client.chats.create(
                model="gemini-3.1-flash-lite-preview",
                config={'system_instruction': self.prompt}
            )

        response = self.session.send_message(message)
    
        return response.text
        
        