"""
TIẾT 4 - NÂNG CAO (45): ATTACHMENT
Kiểm tra loại/kích thước file và lưu file đính kèm xuống ổ đĩa theo từng
hoạt động câu lạc bộ, trả về đường dẫn tương đối để lưu vào database.
"""
import os
import uuid

from fastapi import UploadFile

from config.setting import (
    UPLOAD_DIR,
    MAX_ATTACHMENT_SIZE_MB,
    ALLOWED_ATTACHMENT_EXTENSIONS
)
from exceptions.custom import (
    UnsupportedMediaTypeException,
    PayloadTooLargeException
)

MAX_ATTACHMENT_SIZE_BYTES = MAX_ATTACHMENT_SIZE_MB * 1024 * 1024


def save_activity_attachment(activity_id: int, file: UploadFile) -> dict:
    extension = os.path.splitext(file.filename or "")[1].lower()

    if extension not in ALLOWED_ATTACHMENT_EXTENSIONS:
        raise UnsupportedMediaTypeException(
            f"File extension '{extension}' is not allowed"
        )

    content = file.file.read()

    if len(content) > MAX_ATTACHMENT_SIZE_BYTES:
        raise PayloadTooLargeException(
            f"File exceeds the {MAX_ATTACHMENT_SIZE_MB}MB limit"
        )

    activity_dir = os.path.join(UPLOAD_DIR, str(activity_id))
    os.makedirs(activity_dir, exist_ok= True)

    stored_name = f"{uuid.uuid4().hex}{extension}"
    stored_path = os.path.join(activity_dir, stored_name)

    with open(stored_path, "wb") as output_file:
        output_file.write(content)

    return {
        "file_name" : file.filename,
        "file_path" : stored_path,
        "file_type" : file.content_type or "application/octet-stream",
        "file_size" : len(content)
    }
