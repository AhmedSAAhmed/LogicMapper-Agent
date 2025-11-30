from google.adk.tools.google_search_tool import GoogleSearchTool
from typing import List, Dict, Any
from src.utils.logger import setup_logger

logger = setup_logger("SearchTool")

class SearchTool:
    def __init__(self):
        """Initialize SearchTool using Google ADK's GoogleSearchTool."""
        self.google_search = GoogleSearchTool()
        
    async def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Searches Google using ADK's GoogleSearchTool.
        
        Args:
            query: The search query
            num_results: Number of results to return
            
        Returns:
            List of search results with title, link, and snippet
        """
        try:
            # Use the GoogleSearchTool instance
            search_results = self.google_search(query=query, num_results=num_results)
            
            # Parse the results into a consistent format
            results = []
            if isinstance(search_results, list):
                for item in search_results[:num_results]:
                    results.append({
                        'title': item.get('title', ''),
                        'link': item.get('link', ''),
                        'snippet': item.get('snippet', '')
                    })
            elif isinstance(search_results, str):
                # If it returns a string summary, wrap it
                results.append({
                    'title': 'Search Results',
                    'link': '',
                    'snippet': search_results
                })
            
            logger.info(f"Search completed for '{query}': {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return []
