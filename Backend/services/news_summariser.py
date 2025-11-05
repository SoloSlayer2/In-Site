import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def summarise_news(text: str, topic: str) -> str:
    """Use Gemini to summarize a list of news articles."""
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    prompt = f"""
    Summarize the following recent news articles about '{topic}' 
    into a concise, factual summary(each 5-7 sentences long) in points:

    {text}
    """

    response = model.generate_content(prompt)
    return response.text.strip()
