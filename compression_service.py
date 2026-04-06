import zipfile
import os
import shutil
import logging

def compress_backup(folder_path):

    zip_path = f"{folder_path}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root,file)
                relative_path = os.path.realpath(full_path, folder_path)
                zipf.write(full_path, relative_path)


    shutil.rmtree(folder_path)

    logging.info(f"Backup compressed: {zip_path}")
    print(f"Backup compressed: {zip_path}")
    

       