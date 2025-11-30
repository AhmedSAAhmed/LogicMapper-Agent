import os
import google.generativeai as genai
from typing import List, Dict, Any
from src.utils.logger import setup_logger
from src.tools.file_system import FileSystemTools
from src.tools.search_tool import SearchTool
from src.memory.compressor import ContextCompressor
from src.memory.vector_store import VectorStore

logger = setup_logger("AnalystAgent")

class AnalystAgent:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.model = genai.GenerativeModel(model_name)
        self.search_tool = SearchTool()
        self.compressor = ContextCompressor()
        self.vector_store = VectorStore()

    async def analyze_logic(self, scan_results: Dict[str, Any]) -> List[str]:
        """
        Analyzes the scanned files to extract business logic.
        """
        logger.info("🧠 Analyst starting logic extraction...")
        
        files = scan_results.get("files", [])
        base_path = scan_results.get("path", "")
        
        all_rules = []
        
        for file_rel_path in files:
            full_path = os.path.join(base_path, file_rel_path) if base_path else file_rel_path
            
            # Skip if not a file or if it's too large (basic check)
            if not os.path.exists(full_path):
                continue
                
            content = FileSystemTools.read_file(full_path)
            if not content or content.startswith("Error"):
                continue
            
            # Compress the content to reduce token usage
            file_ext = os.path.splitext(file_rel_path)[1]
            compressed_content = self.compressor.compress(content, file_ext)
                
            logger.info(f"Analyzing file: {file_rel_path}")
            rules = await self._extract_rules_from_file(file_rel_path, compressed_content)
            all_rules.extend(rules)
            
            # Store rules in long-term memory
            if rules:
                self.vector_store.store_rules(rules, metadata={'file': file_rel_path})
            
        logger.info(f"✅ Analysis complete. Extracted {len(all_rules)} rules.")
        return all_rules

    async def _extract_rules_from_file(self, filename: str, content: str) -> List[str]:
        # Check if the code contains any obscure libraries that need research
        search_context = await self._research_unknown_libraries(content)
        
        # Check long-term memory for similar rules
        memory_context = self._get_memory_context(filename)
        
        prompt = f"""
        Analyze the following code file: '{filename}'
        
        Extract all BUSINESS RULES found in this code.
        A business rule is a specific logic statement that dictates how the business operates (e.g., "VIPs get 20% off", "Tax is 5%").
        Ignore boilerplate, imports, and technical setup.
        
        {search_context}
        {memory_context}
        
        Format your response as a simple list of strings, one per line.
        
        Code Content:
        ```
        {content}
        ```
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Basic parsing: split by newlines and clean up
            rules = [line.strip().lstrip('- ').strip() for line in response.text.split('\n') if line.strip()]
            return rules
        except Exception as e:
            logger.error(f"Failed to analyze {filename}: {e}")
            return []
    
    async def _research_unknown_libraries(self, content: str) -> str:
        """
        Searches for information about unknown libraries found in the code.
        """
        # Simple heuristic: look for import statements
        import_lines = [line for line in content.split('\n') if 'import' in line.lower()]
        
        if not import_lines:
            return ""
        
        # Extract library names (simplified)
        libraries = []
        for line in import_lines:
            if 'from' in line:
                parts = line.split('from')[1].split('import')[0].strip()
                libraries.append(parts.split('.')[0])
            elif 'import' in line:
                parts = line.split('import')[1].strip()
                libraries.append(parts.split('.')[0].split(' ')[0])
        
        # Filter to only uncommon libraries (not stdlib)
        common_libs = {'os', 'sys', 'json', 'time', 'datetime', 're', 'math', 'random'}
        uncommon = [lib for lib in libraries if lib not in common_libs]
        
        if not uncommon:
            return ""
        
        # Search for the first uncommon library
        search_results = await self.search_tool.search(f"{uncommon[0]} python library documentation", num_results=2)
        
        if search_results:
            context = "\nAdditional Context from Web Search:\n"
            for result in search_results:
                context += f"- {result['title']}: {result['snippet']}\n"
            return context
        
        return ""
    
    def _get_memory_context(self, filename: str) -> str:
        """
        Retrieves relevant business rules from long-term memory.
        """
        similar_rules = self.vector_store.search_similar_rules(filename, n_results=3)
        
        if similar_rules:
            context = "\nRelevant Business Rules from Memory Bank:\n"
            for rule_data in similar_rules:
                context += f"- {rule_data['rule']}\n"
            logger.info(f"🧠 Recalled {len(similar_rules)} relevant business rules from Memory Bank")
            return context
        
        return ""

import os
