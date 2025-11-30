import os
from typing import Dict, Any, List
from src.utils.logger import setup_logger
from src.tools.file_system import FileSystemTools

logger = setup_logger("ScannerAgent")

class ScannerAgent:
    def __init__(self, model_name: str = None):
        # Model name is accepted for consistency but not strictly needed for basic scanning
        self.model_name = model_name

    async def scan_repository(self, repo_path: str) -> Dict[str, Any]:
        """
        Scans the repository using FileSystemTools.
        """
        logger.info(f"🔍 Scanning path: {repo_path}")
        
        files = FileSystemTools.list_files(repo_path)
        
        # Filter out non-code files for this demo
        code_files = [f for f in files if f.endswith(('.py', '.java', '.js', '.ts', '.cpp', '.h'))]
        
        languages = self._identify_languages(code_files)
        
        logger.info(f"✅ Found {len(code_files)} code files.")
        
        return {
            "path": repo_path,
            "files": code_files,
            "languages": languages,
            "summary": f"Scanned {len(code_files)} files. Languages: {', '.join(languages.keys())}"
        }

    def _identify_languages(self, files: List[str]) -> Dict[str, int]:
        extensions = {}
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext:
                extensions[ext] = extensions.get(ext, 0) + 1
        return extensions
