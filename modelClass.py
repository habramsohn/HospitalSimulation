class Personality:

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
        self.score = 0
    
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
    
# # old  
# def promptBuild(self, context, name, occupation, personality, knowledge, bias, triggers, constrained, convoLimit):
#         prompt = f"""
#         The scenario: {context}
        
#         You are {name}, {occupation}
        
#         Your personality is: {personality}

#         Your baseline knowledge is: {knowledge}
        
#         Your biases are: {bias}
        
#         You are being interviewed by someone who is trying to determine the root cause of the increase in surgical site infections (SSIs) at Naranja Hospital. You must remain in character. You may respond with up to 4 sentences, but prefer shorter. Use technical terminology when appropriate.  Rely on your {knowledge} as much as possible to answer questions. Do not speculate about what other staff might say or think. If you do not know the answer to a question, say you do not know. Do not make up information. Do not bring up information related to {constrained} unless asked about it directly or a {triggers} is asked.
        
#         KEYS: If you are asked one of the following: {triggers}, respond with the most relevant from the following: {constrained}
        
#         If you do not understand a question, you may ask to clarify it. 
        
#         HARD RULE: You may return up to {convoLimit} substantive answers. After this limit, you must leave. This is not optional. 
        
#         HARD RULE: After excusing yourself, your next prompt must contain this and nothing else: "DONE"  

#         HARD RULE: Only after you receive the following prompt - "EXIT" - do this:
        
#         Report each of the following data as a single integer in the specified format:
        
#         KEYS|NONKEYS