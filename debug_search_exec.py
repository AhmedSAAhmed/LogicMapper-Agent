import asyncio
from google.adk.tools.google_search_tool import GoogleSearchTool

async def test_search():
    tool = GoogleSearchTool()
    try:
        # Try 'query' as the argument name
        result = await tool.run_async(args={'query': 'python programming'}, tool_context=None)
        print("Result:", result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_search())
