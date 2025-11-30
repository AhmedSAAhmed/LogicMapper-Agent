import os
import asyncio
import argparse
from dotenv import load_dotenv

# --- CHANGED: Using the AI Studio SDK (Simpler, Free Tier friendly) ---
import google.generativeai as genai

# LogicMapper Internal Imports
from src.agents.orchestrator import OrchestratorAgent
from src.utils.logger import setup_logger

# Setup Observability
logger = setup_logger("LogicMapper_Main")

def init_app():
    """Initializes the Google Gemini API Environment"""
    load_dotenv()
    
    # We only need the API Key now, not the Project ID
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("❌ GOOGLE_API_KEY not found in .env file. Get one at https://aistudio.google.com/")

    # Configure the global SDK with your key
    genai.configure(api_key=api_key)
    logger.info(f"✅ Google AI Studio Configured successfully.")

async def run_modernization_task(repo_url: str):
    """
    The Main Workflow:
    1. Orchestrator receives the Repo
    2. Spawns Scanners (Parallel)
    3. Spawns Analyst (Sequential)
    4. Returns Report
    """
    logger.info(f"🚀 Starting Modernization Task for: {repo_url}")

    # Initialize the Brain (The Orchestrator)
    # Note: AI Studio uses "gemini-1.5-pro-latest" or similar model names
    orchestrator = OrchestratorAgent(model_name="gemini-1.5-pro-latest")

    try:
        # Run the Agentic Workflow
        final_report = await orchestrator.process_repository(repo_url)
        
        # Output the result
        print("\n" + "="*50)
        print("🎉 MODERNIZATION STRATEGY GENERATED")
        print("="*50)
        print(final_report)
        print("="*50 + "\n")
        
        # Save output
        with open("final_report.md", "w", encoding='utf-8') as f:
            f.write(final_report)
            logger.info("💾 Report saved to final_report.md")

    except Exception as e:
        logger.error(f"❌ Workflow Failed: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LogicMapper CLI")
    parser.add_argument("--repo", type=str, required=True, help="URL or Path to legacy code")
    
    args = parser.parse_args()
    
    # Run the setup
    try:
        init_app()
        # Run the async workflow
        asyncio.run(run_modernization_task(args.repo))
    except Exception as e:
        print(f"Critical Error: {e}")