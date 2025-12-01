import logging
import sys
import io

def setup_logger(name: str = "LogicMapper") -> logging.Logger:
    """
    Sets up a logger with a standard configuration.
    
    Args:
        name: The name of the logger.
        
    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    
    # Prevent adding multiple handlers if function is called multiple times
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.INFO)
    
    # Create console handler with UTF-8 encoding support
    # This prevents UnicodeEncodeError when logging emoji characters on Windows
    try:
        # Wrap stdout with UTF-8 encoding, replacing unencodable characters
        utf8_stdout = io.TextIOWrapper(
            sys.stdout.buffer,
            encoding='utf-8',
            errors='replace',  # Replace unencodable characters with '?'
            line_buffering=True
        )
        handler = logging.StreamHandler(utf8_stdout)
    except (AttributeError, io.UnsupportedOperation):
        # Fallback to regular stdout if wrapping fails
        handler = logging.StreamHandler(sys.stdout)
    
    handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
