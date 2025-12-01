import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# LogicMapper Imports
from src.agents.orchestrator import OrchestratorAgent

async def test_crash():
    """Test the crash scenario."""
    print("Starting test...")
    orchestrator = OrchestratorAgent(model_name="gemini-2.0-flash")
    
    print("Processing repository...")
    try:
        final_report = await orchestrator.process_repository("test_legacy_code.py")
        print("Success!")
        print(final_report)
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_crash())
