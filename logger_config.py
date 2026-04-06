import logging
from config import LOG_FLIE

def setup_logging():
    logging.basicConfig(
        filename=LOG_FLIE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )