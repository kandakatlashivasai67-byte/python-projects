import logging

def setup_logger():
    logging.basicConfig(
        filename="email_log.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
