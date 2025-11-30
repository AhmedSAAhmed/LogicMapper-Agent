import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
from src.tools.search_tool import SearchTool
from src.utils.logger import setup_logger

logger = setup_logger("SearchToolTest")

async def test_search_tool():
    """Test the SearchTool to verify it works with Google ADK."""
    
    # Initialize environment
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    
    logger.info("Initializing SearchTool...")
    search_tool = SearchTool()
    
    # Test query
    test_query = "Python FastAPI framework documentation"
    logger.info(f"Testing search with query: '{test_query}'")
    
    try:
        results = await search_tool.search(test_query, num_results=3)
        
        if results:
            logger.info(f"✅ Search successful! Found {len(results)} results:")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['title']}")
                print(f"   Link: {result['link']}")
                print(f"   Snippet: {result['snippet'][:100]}...")
        else:
            logger.warning("⚠️ No results returned from search")
            
    except Exception as e:
        logger.error(f"❌ Search test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("="*60)
    print("Testing SearchTool with Google ADK")
    print("="*60)
    asyncio.run(test_search_tool())
    print("="*60)
