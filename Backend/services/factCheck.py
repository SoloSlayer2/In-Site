import os

import google.generativeai as genai
from dotenv import load_dotenv
import requests


load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
# Initialize clients
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def search_with_serper(query: str, num_results: int = 5) -> str:
    """Perform a Google search using Serper.dev and return summarized text."""
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY}
    payload = {"q": query, "num": num_results}

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        results = data.get("organic", [])
        context = "\n".join(
            f"- {r['title']}: {r.get('snippet', '')}\n Source:{r['link']}"
            for r in results
        )

        return context or "No relevant articles found."
    except Exception as e:
        return f"Error during search: {str(e)}"

def check_news(news: str, context: str) -> str:
    """
    Uses Gemini 2.5 Flash Lite to classify a news claim as:
    - True
    - Partially True
    - False
    
    Based only on the provided web search context.
    """
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    prompt = f"""
    You are a fact verification assistant.

    Analyze the following news claim using ONLY the web search results provided.

    News claim:
    "{news}"

    Web search context:
    {context}

    Task:
    - Read the claim and compare it carefully with the information in the web search context.
    - Decide whether the claim is True, Partially True, or False.
    - Follow these rules strictly:
        * "True" → The claim matches the web context fully and is confirmed by multiple sources.
        * "Partially True" → The claim contains some truth, but is incomplete, exaggerated, or lacks context.
        * "False" → The claim is directly contradicted by the web context or unsupported by reliable sources.
    - Do NOT invent information.
    - Base your verdict strictly on the text in the context.

    Respond ONLY with one word:
    True
    Partially True
    or
    False
    """

    response = model.generate_content(prompt)
    verdict = response.text.strip().replace('"', '')

    # sanitize output (in case model gives extra text)
    if "partially" in verdict.lower():
        verdict = "Partially True"
    elif "true" in verdict.lower():
        verdict = "True"
    elif "false" in verdict.lower():
        verdict = "False"
    else:
        verdict = "Uncertain"

    return verdict

def summarize_with_context(news: str, context: str) -> dict:
    """
    Use Gemini to summarize what the internet says about a given news claim.
    The model does NOT judge correctness — it only summarizes the search results.
    """
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are a helpful fact-assistant.

    The following news claim was found online:
    "{news}"

    Below are recent search results about this topic:
    {context}

    Your task:
    - Summarize what the search results collectively say about this topic.
    - Highlight the key facts and common points found across multiple sources.
    - Keep the tone neutral and concise.
    - Do NOT give a verdict (true or false).
    - Do NOT hallucinate or infer beyond the context.
    - Cite the sources provided to you along with the context
    - The language of the answer must be same with that of the question.
    """

    response = model.generate_content(prompt)
    return response.text
