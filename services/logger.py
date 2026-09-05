from __future__ import annotations

import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """Return a configured logger with standard stream handling (warnings/errors only)."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.WARNING)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.WARNING)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    return logger
