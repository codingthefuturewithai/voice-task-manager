#!/usr/bin/env python3
"""
Test GPT-5-nano's ability to match task names with variations
Simplified version
"""

import os
from openai import OpenAI

# Get API key from environment
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Please set OPENAI_API_KEY environment variable")
    exit(1)

client = OpenAI(api_key=api_key)

# The actual task name
task = "go to grocery store"

# Various ways users might say it
test_commands = [
    "Mark go-to-grocery-store task complete",
    "Complete the go to grocery store task",
    "I finished go-to-grocery-store", 
    "Done with grocery store",
    "Check off go to the grocery store",
    "Mark grocery shopping complete",
    "Complete go-to-store task"
]

print("=" * 60)
print("Testing GPT-5-nano task matching (simplified)")
print("=" * 60)

for command in test_commands:
    print(f"\nCommand: '{command}'")
    
    # Much simpler prompt
    prompt = f"""Task: go to grocery store

User said: {command}

Is the user referring to the task above? Reply: YES or NO"""

    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        result = response.choices[0].message.content.strip()
        
        if "YES" in result.upper():
            print(f"✅ Matched correctly")
        else:
            print(f"❌ Failed to match: {result}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

print("\n" + "=" * 60)
print("Now testing if GPT-5-nano understands hyphen variations")
print("=" * 60)

# Direct test about hyphens
prompt = """Are these referring to the same thing?
1. "go to grocery store"
2. "go-to-grocery-store"

Answer: YES or NO"""

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[{"role": "user", "content": prompt}]
)

print(f"Are 'go to grocery store' and 'go-to-grocery-store' the same?")
print(f"GPT-5-nano says: {response.choices[0].message.content}")