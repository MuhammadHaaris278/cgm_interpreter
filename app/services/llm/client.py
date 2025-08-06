import os
from openai import OpenAI
from app.config.loader import Config

# Load config
config = Config()

client = OpenAI(
    base_url=config.llm_base_url,
    api_key=config.llm_api_key
)

def get_openai_client():
    return client
