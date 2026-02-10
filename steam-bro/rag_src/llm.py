import google.generativeai as genai
import os
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class Gemini:
    def __init__(self) -> None:
        self.model = genai.GenerativeModel("models/gemma-3-12b-it")
    
    def ask_gemini(self , prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as  e:
            print("error while asking gemini : " , e)
        return "no response found from our llm we can try it later" 