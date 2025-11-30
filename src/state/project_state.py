from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import json
import os
from datetime import datetime
from src.utils.logger import setup_logger

logger = setup_logger("ProjectState")

class FileAnalysis(BaseModel):
    """Represents the analysis status and results for a single file."""
    file_path: str
    language: str
    business_rules: List[str] = []
    status: str = "pending"  # pending, analyzed, error

class ProjectState(BaseModel):
    """
    Central state management for the LogicMapper project.
    Tracks progress, stores results, and persists state to disk.
    """
    project_name: str = "LogicMapper Project"
    repo_path: str
    start_time: datetime = Field(default_factory=datetime.now)
    scanned_files: List[str] = []
    analyses: Dict[str, FileAnalysis] = {}
    modernization_plan: Optional[str] = None
    dependency_graph: Optional[str] = None
    
    def update_scan_results(self, scan_results: Dict[str, Any]):
        """Update state with results from the Scanner Agent."""
        self.scanned_files = scan_results.get("files", [])
        base_path = scan_results.get("path", "")
        
        for file_rel_path in self.scanned_files:
            # Use relative path as key
            if file_rel_path not in self.analyses:
                ext = os.path.splitext(file_rel_path)[1]
                self.analyses[file_rel_path] = FileAnalysis(
                    file_path=file_rel_path, 
                    language=ext
                )
        logger.info(f"📊 State updated: {len(self.scanned_files)} files found.")

    def update_analysis(self, file_path: str, rules: List[str]):
        """Update state with results from the Analyst Agent."""
        if file_path in self.analyses:
            self.analyses[file_path].business_rules = rules
            self.analyses[file_path].status = "analyzed"
            logger.info(f"✅ Analysis recorded for {file_path}")
        else:
            # Handle case where file wasn't in initial scan (unlikely but possible)
            ext = os.path.splitext(file_path)[1]
            self.analyses[file_path] = FileAnalysis(
                file_path=file_path,
                language=ext,
                business_rules=rules,
                status="analyzed"
            )
            logger.warning(f"⚠️ File {file_path} added to state during analysis phase.")

    def set_modernization_plan(self, plan: str):
        """Store the final modernization plan."""
        self.modernization_plan = plan
        logger.info("📝 Modernization plan stored in state.")

    def save_to_json(self, filename: str = "project_state.json"):
        """Persist the current state to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.model_dump_json(indent=2))
            logger.info(f"💾 Project state saved to {filename}")
        except Exception as e:
            logger.error(f"❌ Failed to save state: {e}")

    @classmethod
    def load_from_json(cls, filename: str = "project_state.json") -> Optional['ProjectState']:
        """Load project state from a JSON file."""
        try:
            if not os.path.exists(filename):
                return None
            with open(filename, 'r', encoding='utf-8') as f:
                data = f.read()
            return cls.model_validate_json(data)
        except Exception as e:
            logger.error(f"❌ Failed to load state: {e}")
            return None
