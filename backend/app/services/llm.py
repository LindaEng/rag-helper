import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in .env file")
            cls._instance.client = Groq(api_key=api_key)
        return cls._instance
    
    def generate(self, question: str, context: str) -> str:
        print(f"Question: {question[:50]}...")  # Debug
        print(f"Context length: {len(context)}")  # Debug
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": f"Answer based ONLY on this context...\n\nContext:\n{context}"
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                temperature=0.3
            )
            answer = response.choices[0].message.content
            print(f"Answer: {answer[:100]}...")  # Debug
            return answer
        except Exception as e:
            print(f"ERROR in llm.py: {e}")  # Debug
            return f"Error: {str(e)}"

llm_service = LLMService()