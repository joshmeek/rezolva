import logging
from typing import Dict, Any

def setup_logger(config: Dict[str, Any]) -> logging.Logger:
    logger = logging.getLogger('tiny_er')
    level = config.get('log_level', 'INFO')
    logger.setLevel(level)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(ch)

    # File handler (optional)
    if 'log_file' in config:
        fh = logging.FileHandler(config['log_file'])
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

class EntityResolutionLogger:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def log_start(self, num_entities: int):
        self.logger.info(f"Starting entity resolution process with {num_entities} entities")

    def log_blocking(self, num_blocks: int):
        self.logger.info(f"Blocking complete. Created {num_blocks} blocks")

    def log_comparison(self, num_comparisons: int):
        self.logger.info(f"Comparison phase complete. Performed {num_comparisons} comparisons")

    def log_matching(self, num_matches: int):
        self.logger.info(f"Matching phase complete. Found {num_matches} matches")

    def log_error(self, error_message: str):
        self.logger.error(f"Error occurred: {error_message}")

    def log_warning(self, warning_message: str):
        self.logger.warning(warning_message)

    def log_custom(self, message: str, level: str = 'INFO'):
        log_method = getattr(self.logger, level.lower())
        log_method(message)

def create_logger(config: Dict[str, Any]) -> EntityResolutionLogger:
    logger = setup_logger(config)
    return EntityResolutionLogger(logger)