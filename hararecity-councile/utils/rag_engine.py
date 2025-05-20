import os
from typing import Tuple, List
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

class ChatEngine:
    def __init__(self):
        # Check for required environment variables
        if not os.getenv("GROQ_API_KEY"):
            raise ValueError(
                "Missing required environment variable: GROQ_API_KEY\n"
                "Please create a .env file with this variable or set it in your environment."
            )
        
        # Initialize Groq chat model
        self.chat_model = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama2-70b-4096",
            temperature=0.7,
            max_tokens=1024,
            request_timeout=60
        )
        
        # Initialize memory with correct key
        self.memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )
        
        # System prompt for the chatbot
        system_prompt = """You are the Harare City Council's internal IT support chatbot. Your role is to:
1. Help employees with their IT-related queries within the organization
2. Provide clear, professional, and accurate responses
3. If you're unsure about an answer or if the query is too complex, acknowledge this and suggest involving a human IT support staff member
4. Maintain a helpful and professional tone
5. Focus on IT-related topics such as:
   - Software and hardware issues
   - Network and connectivity problems
   - Account and access management
   - IT policies and procedures
   - General IT guidance

Remember to:
- Be clear when you need to escalate to human support
- Provide step-by-step instructions when possible
- Ask for clarification if the query is unclear
- Maintain confidentiality and security awareness
"""
        
        # Initialize conversation chain
        self.conversation = ConversationChain(
            llm=self.chat_model,
            memory=self.memory,
            verbose=True
        )
        
        # Set the system prompt
        self.conversation.prompt.template = f"{system_prompt}\n\nCurrent conversation:\n{{history}}\nHuman: {{input}}\nAssistant:"

    def get_response(self, query: str) -> Tuple[str, List[str]]:
        """
        Get response for a user query.
        
        Args:
            query (str): User's question
            
        Returns:
            Tuple[str, List[str]]: Generated response and empty sources list
        """
        # Get response from conversation chain
        response = self.conversation.predict(input=query)
        
        return response, []  # Return empty sources list for compatibility 