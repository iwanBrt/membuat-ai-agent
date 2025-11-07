from openai import OpenAI
import os
import math
import json
from dotenv import load_dotenv  
import requests
from ddgs import DDGS
import trafilatura

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
#trafilatura
MODEL = "gpt-4o-mini"

def web_search(query_text: str, maximum_reslult: int = 5):
    search_results = []
    with DDGS() as search_engine:
        for result in search_engine.text(query_text, maximum_reslult=maximum_reslult):
            search_results.append({
                'title': result.get('title'),
                'url': result.get('href'),
                'snippet': result.get('body'),
                'source': 'duckduckgo'
            })
            
    return search_results

def fetch_webpage_content(url: str,max_caracters: int = 4000):
    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent': 'Mozilla/5.0 (compatible: WebResearchBot/1.0)"}
            
        )
        
        response.raise_for_status()
        
    extrscted_text= trafilatura.extract(
        response.text,
        include_comments=False,
        include_tables=False
    )
    
    if not extrscted_text:
        return {'url': url, 'ok': False, 'reason': 'gagal extract conten'}
    