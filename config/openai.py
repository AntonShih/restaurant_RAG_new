import os
import openai
from dotenv import load_dotenv

load_dotenv()

def init_openai():
    """初始化 OpenAI"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
