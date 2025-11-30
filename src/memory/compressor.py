import re
from typing import Dict, List
from src.utils.logger import setup_logger

logger = setup_logger("Compressor")

class ContextCompressor:
    """
    Compresses code context by removing comments, empty lines, and unnecessary whitespace.
    This reduces token usage when sending large legacy files to the LLM.
    """
    
    def __init__(self):
        self.language_handlers = {
            '.py': self._compress_python,
            '.java': self._compress_java,
            '.js': self._compress_javascript,
            '.ts': self._compress_javascript,
            '.cpp': self._compress_c_style,
            '.c': self._compress_c_style,
            '.h': self._compress_c_style,
        }
    
    def compress(self, content: str, file_extension: str) -> str:
        """
        Compresses code content based on file type.
        
        Args:
            content: The raw code content
            file_extension: File extension (e.g., '.py', '.java')
            
        Returns:
            Compressed code content
        """
        handler = self.language_handlers.get(file_extension, self._compress_generic)
        compressed = handler(content)
        
        original_lines = len(content.split('\n'))
        compressed_lines = len(compressed.split('\n'))
        reduction = ((original_lines - compressed_lines) / original_lines * 100) if original_lines > 0 else 0
        
        logger.info(f"Compressed {file_extension} file: {original_lines} → {compressed_lines} lines ({reduction:.1f}% reduction)")
        
        return compressed
    
    def _compress_python(self, content: str) -> str:
        """Compress Python code."""
        lines = content.split('\n')
        compressed_lines = []
        
        in_multiline_string = False
        multiline_delimiter = None
        
        for line in lines:
            stripped = line.strip()
            
            # Handle multiline strings
            if '"""' in line or "'''" in line:
                if not in_multiline_string:
                    multiline_delimiter = '"""' if '"""' in line else "'''"
                    in_multiline_string = True
                elif multiline_delimiter in line:
                    in_multiline_string = False
                compressed_lines.append(line)
                continue
            
            if in_multiline_string:
                compressed_lines.append(line)
                continue
            
            # Skip comments and empty lines
            if not stripped or stripped.startswith('#'):
                continue
            
            # Remove inline comments (but preserve strings)
            if '#' in line and not self._is_in_string(line, line.index('#')):
                line = line[:line.index('#')].rstrip()
            
            compressed_lines.append(line)
        
        return '\n'.join(compressed_lines)
    
    def _compress_java(self, content: str) -> str:
        """Compress Java code."""
        # Remove single-line comments
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        
        # Remove multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Remove empty lines
        lines = [line for line in content.split('\n') if line.strip()]
        
        return '\n'.join(lines)
    
    def _compress_javascript(self, content: str) -> str:
        """Compress JavaScript/TypeScript code."""
        # Remove single-line comments
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        
        # Remove multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Remove empty lines
        lines = [line for line in content.split('\n') if line.strip()]
        
        return '\n'.join(lines)
    
    def _compress_c_style(self, content: str) -> str:
        """Compress C/C++ code."""
        # Remove single-line comments
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        
        # Remove multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Remove preprocessor comments
        content = re.sub(r'#\s*//.*?$', '', content, flags=re.MULTILINE)
        
        # Remove empty lines
        lines = [line for line in content.split('\n') if line.strip()]
        
        return '\n'.join(lines)
    
    def _compress_generic(self, content: str) -> str:
        """Generic compression - just remove empty lines."""
        lines = [line for line in content.split('\n') if line.strip()]
        return '\n'.join(lines)
    
    def _is_in_string(self, line: str, position: int) -> bool:
        """Check if a position in a line is inside a string literal."""
        in_single = False
        in_double = False
        
        for i, char in enumerate(line[:position]):
            if char == "'" and (i == 0 or line[i-1] != '\\'):
                in_single = not in_single
            elif char == '"' and (i == 0 or line[i-1] != '\\'):
                in_double = not in_double
        
        return in_single or in_double
    
    def get_compression_stats(self, original: str, compressed: str) -> Dict[str, int]:
        """Get statistics about compression."""
        return {
            'original_lines': len(original.split('\n')),
            'compressed_lines': len(compressed.split('\n')),
            'original_chars': len(original),
            'compressed_chars': len(compressed),
            'reduction_percent': round((1 - len(compressed) / len(original)) * 100, 2) if len(original) > 0 else 0
        }
