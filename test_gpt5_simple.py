#!/usr/bin/env python3
"""
Simple test of GPT-5-nano 
"""

import os
from openai import OpenAI

# Get API key from environment
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Please set OPENAI_API_KEY environment variable")
    exit(1)

client = OpenAI(api_key=api_key)

print("Testing GPT-5-nano with simple prompt...")
print("=" * 60)

try:
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "user", "content": "Say 'hello world'"}
        ]
    )
    
    print(f"Response: '{response.choices[0].message.content}'")
    
except Exception as e:
    print(f"Error: {e}")

print("\nNow testing with task matching...")
print("=" * 60)

try:
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "user", "content": """Match this command to a task.

Tasks:
- go to grocery store
- buy milk

Command: "complete grocery store"

Reply with just the task name."""}
        ]
    )
    
    print(f"Response: '{response.choices[0].message.content}'")
    
except Exception as e:
    print(f"Error: {e}")