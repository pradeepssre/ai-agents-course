import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic()
response = client.messages.create(
    model='claude-sonnet-4-20250514',
    max_tokens=50,
    messages=[{'role': 'user', 'content': 'Say hello in 5 words or less'}]
)
print('API working:', response.content[0].text)