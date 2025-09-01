#!/usr/bin/env python3
"""
Test GPT-5-nano's ability to match task names with variations
like hyphens, spaces, different phrasings
"""

import os
from openai import OpenAI

# Get API key from environment
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Please set OPENAI_API_KEY environment variable")
    exit(1)

client = OpenAI(api_key=api_key)

# Test cases with the actual task list
tasks = [
    "Sign and return equity agreement",
    "Complete V1 of new cloud code sub-agent workflow", 
    "Review Coding the Future subscriptions and remove unnecessary ones",
    "Set up Coding the Future with Coinbase",
    "go to grocery store",  # The actual task name
    "Plan Florida vacation"
]

# Various ways users might say the same task
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
print("Testing GPT-5-nano task matching capabilities")
print("=" * 60)

for command in test_commands:
    print(f"\nUser command: '{command}'")
    print("-" * 40)
    
    prompt = f"""You are a task manager assistant. A user wants to mark a task as complete.

Available tasks:
{chr(10).join(f'- {task}' for task in tasks)}

User said: "{command}"

Which task are they trying to complete? Reply with ONLY the exact task name from the list above, or "NO_MATCH" if you can't determine which task they mean.

Important: Be flexible with matching. Users might:
- Add or remove hyphens (go-to-store vs go to store)
- Use synonyms (grocery store, groceries, shopping)
- Use partial names
- Add extra words like "task" or "the"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "You match user commands to tasks. Be flexible with variations."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=100
        )
        
        result = response.choices[0].message.content.strip()
        
        # Debug: show raw response
        print(f"Raw response: '{response.choices[0].message.content}'")
        
        # Check if it matched correctly
        if result == "go to grocery store":
            print(f"✅ CORRECT: Matched '{result}'")
        elif result == "NO_MATCH":
            print(f"❌ FAILED: Could not match")
        else:
            print(f"⚠️  MATCHED: '{result}' (different task)")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

print("\n" + "=" * 60)
print("Test complete!")
print("=" * 60)