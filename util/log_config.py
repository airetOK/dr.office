import sys
import logging


def load_log_config(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    stdout = logging.StreamHandler(stream=sys.stdout)
    fmt = logging.Formatter(
        "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%SZ"
    )
    stdout.setFormatter(fmt)
    logger.addHandler(stdout)
    logger.setLevel(logging.INFO)
    return logger