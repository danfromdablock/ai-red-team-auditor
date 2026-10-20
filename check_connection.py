"""Quick test: is your API key working? Run:  python check_connection.py"""
import sys

from auditor import active_provider, ask_ai, model_name

provider = active_provider()
if not provider:
    print("❌ No API key found. Open your .env file and paste your key after GEMINI_API_KEY= (or GROQ_API_KEY=)")
    sys.exit(1)

print(f"Testing {provider} ({model_name()})...")
try:
    reply = ask_ai("Say hello in one word.", json_mode=False, max_tokens=1024)
    print(f"✅ {provider.title()} is working! The AI said: {reply.strip()}")
except Exception as e:
    print(f"❌ {provider.title()} did not answer: {e}")
    sys.exit(1)
