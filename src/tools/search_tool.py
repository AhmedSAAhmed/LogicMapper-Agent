from googlesearch import search as google_search
from typing import List, Dict, Any
from src.utils.logger import setup_logger
import asyncio

logger = setup_logger("SearchTool")

class SearchTool:
    def __init__(self):
        """Initialize SearchTool."""
        pass
        
    async def search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Searches Google using googlesearch-python.
        
        Args:
            query: The search query
            num_results: Number of results to return
            
        Returns:
            List of search results with title, link, and snippet
        """
        try:
            # Run the synchronous search in a thread pool to avoid blocking asyncio loop
            results = await asyncio.to_thread(self._sync_search, query, num_results)
            
            logger.info(f"Search completed for '{query}': {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return []

    def _sync_search(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """Synchronous search function to be run in thread."""
        results = []
        try:
            # googlesearch-python returns objects with title, description, url
            search_results = google_search(query, num_results=num_results, advanced=True)
            
            for item in search_results:
                results.append({
                    'title': item.title,
                    'link': item.url,
                    'snippet': item.description
                })
        except Exception as e:
            logger.error(f"Sync search error: {e}")
            
        return results
