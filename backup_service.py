import os
import shutil
import logging
from datetime import datetime
from config import Data_Format
from file_utlis import ensure_dir, get_file_hash


def run_backup(source, destination, dry_run=False):
    timestamp = Datetime.now().strftie(Data_Format)
    backup_folder = os.path.join(destination, f"backup_{timestamp}")

    ensure_dir(backup_folder)

    logging.info("Backup started")

    for root, dirs, files in os.walk(source):

        for file in files:
            source_file = os.path.join(root, file)
            relative_path = os.path.relpath(source_file, source)
            dest_file = os.path.join(backup_folder, relative_path)

            ensure_dir(os.path.dirname(dest_file))

            if not os.path.exists(dest_file) or \
                get_file_hash(source_file) != get_file_hash(dest_file):

                if fet_run:
                    print(f"[dry_run] Would copy:{relative_path}")
                else:
                    shutil.copy2(source_file, dest_file)
                    logging.ingo(f"Copied: {relative_path}")

        logging.info("Backup completed")
        print("Backup completed")

        return backup_folder































