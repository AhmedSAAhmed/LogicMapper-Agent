import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.adk.tools.google_search_tool import google_search

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("="*60)
print("Testing google_search function directly")
print("="*60)

try:
    print("\nCalling google_search...")
    result = google_search(query="Python FastAPI framework", num_results=3)
    
    print(f"\nResult type: {type(result)}")
    print(f"\nResult content:\n{result}")
    
    if isinstance(result, list):
        print(f"\nList length: {len(result)}")
        for i, item in enumerate(result):
            print(f"\nItem {i}: {type(item)}")
            print(item)
    
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
