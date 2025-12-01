import asyncio
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

print(f"Python version: {sys.version}")
print(f"asyncio.to_thread available: {hasattr(asyncio, 'to_thread')}")

# LogicMapper Imports
from src.agents.orchestrator import OrchestratorAgent

async def test_crash():
    """Test the crash scenario."""
    print("Starting test...")
    try:
        orchestrator = OrchestratorAgent(model_name="gemini-2.0-flash")
        
        print("Processing repository...")
        final_report = await orchestrator.process_repository("test_legacy_code.py")
        print("Success!")
        print(final_report[:200])
    except Exception as e:
        print(f"\n\n=== ERROR OCCURRED ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")
        print(f"\n=== FULL TRACEBACK ===")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_crash())
