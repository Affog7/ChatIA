# ============================================================================
# FILE: utils/logger.py
# ============================================================================
import logging
import sys
from config import Config

def setup_logger(name: str) -> logging.Logger:
    """Configure et retourne un logger"""
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, Config().LOG_LEVEL))
    
    # Handler pour la console
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    
    # Format des logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger
