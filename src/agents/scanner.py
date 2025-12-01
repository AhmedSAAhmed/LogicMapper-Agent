import os
import tempfile
import subprocess
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
        If repo_path is a URL, clones it first.
        """
        logger.info(f"🔍 Scanning path: {repo_path}")
        
        # Check if it's a git URL
        actual_path = repo_path
        cloned = False
        
        if self._is_git_url(repo_path):
            logger.info(f"📥 Detected git repository URL, cloning...")
            actual_path = self._clone_repository(repo_path)
            cloned = True
            logger.info(f"✅ Repository cloned to: {actual_path}")
        
        files = FileSystemTools.list_files(actual_path)
        
        # Filter out non-code files for this demo
        code_files = [f for f in files if f.endswith(('.py', '.java', '.js', '.ts', '.cpp', '.h'))]
        
        languages = self._identify_languages(code_files)
        
        logger.info(f"✅ Found {len(code_files)} code files.")
        
        return {
            "path": actual_path,
            "files": code_files,
            "languages": languages,
            "summary": f"Scanned {len(code_files)} files. Languages: {', '.join(languages.keys())}",
            "cloned": cloned
        }

    def _is_git_url(self, path: str) -> bool:
        """Check if the path is a git repository URL."""
        return path.startswith(('http://', 'https://', 'git@', 'git://'))

    def _clone_repository(self, repo_url: str) -> str:
        """Clone a git repository to a temporary directory."""
        # Create a unique temp directory name but don't create it yet
        # Git clone will create it
        temp_base = tempfile.gettempdir()
        import uuid
        temp_dir = os.path.join(temp_base, f"logicmapper_repo_{uuid.uuid4().hex[:8]}")
        
        try:
            # Clone the repository - git will create the directory
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', repo_url, temp_dir],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                logger.error(f"Git clone failed: {result.stderr}")
                raise Exception(f"Failed to clone repository: {result.stderr}")
            
            return temp_dir
            
        except subprocess.TimeoutExpired:
            logger.error("Git clone timed out")
            raise Exception("Repository clone timed out after 5 minutes")
        except Exception as e:
            logger.error(f"Error cloning repository: {e}")
            raise

    def _identify_languages(self, files: List[str]) -> Dict[str, int]:
        extensions = {}
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext:
                extensions[ext] = extensions.get(ext, 0) + 1
        return extensions
