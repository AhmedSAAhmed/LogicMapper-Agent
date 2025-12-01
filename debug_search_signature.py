from google.adk.tools.google_search_tool import GoogleSearchTool
import inspect

tool = GoogleSearchTool()
print(inspect.signature(tool.run_async))
