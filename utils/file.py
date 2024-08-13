from fastapi import UploadFile
import os
import re
from datetime import datetime


def regularize_file_name(file_name: str) -> str:
    return re.sub(r"[^\w.]", "_", file_name)


def save_file(file: UploadFile) -> str:
    name, ext = os.path.splitext(file.filename)
    name = regularize_file_name(name)
    file_name = os.path.join("uploads", f"{name}_{datetime.now().isoformat()}{ext}")
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    with open(file_name, "wb") as f:
        f.write(file.file.read())
    return file_name


def delete_file(file_path: str):
    os.remove(file_path)
    return True
