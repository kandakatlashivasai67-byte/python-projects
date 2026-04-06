import os
import hashlib

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, "rb")as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()