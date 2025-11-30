import os
from typing import List, Dict, Any

class FileSystemTools:
    @staticmethod
    def list_files(path: str) -> List[str]:
        """
        Lists all files in a directory recursively.
        """
        file_list = []
        if os.path.isfile(path):
            return [path]
            
        for root, dirs, files in os.walk(path):
            if ".git" in dirs:
                dirs.remove(".git")
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list

    @staticmethod
    def read_file(path: str) -> str:
        """
        Reads the content of a file.
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
