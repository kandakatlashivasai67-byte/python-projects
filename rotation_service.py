import os
import shutil
import logging
from config import max_backups

def rotate_backups(destination, retention=MAX_BACKUPS):

    backups = sorted([
        os.path.join(destination, folder)
        for folder in os.listdir(destination)
        if folder.startswith("backup_")
    ])

    while len(backups) > retention:
        oldest = backups.pop(0)
        shutil.rmtree(oldest)
        logging.info(f"Deleted old backup: {oldest}")
        print(f"Deleted old backup: {oldest_bacakup}")
