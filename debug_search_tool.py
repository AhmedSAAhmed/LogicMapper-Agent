from google.adk.tools.google_search_tool import GoogleSearchTool
import inspect

try:
    tool = GoogleSearchTool()
    print("Attributes of GoogleSearchTool:")
    print(dir(tool))
    print("\nMethods:")
    for name, method in inspect.getmembers(tool, predicate=inspect.ismethod):
        print(name)
except Exception as e:
    print(f"Error: {e}")
