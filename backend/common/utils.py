import base64
import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename
from .config import allowed_file

def encode_filename(filename):
    # 将文件名编码为 base64 字符串
    return base64.urlsafe_b64encode(filename.encode('utf-8')).decode('utf-8')

def upload_images(file, type_id, upload_type="comments"):
    if file and allowed_file(file.filename):
        original_filename = file.filename
        file_extension = os.path.splitext(original_filename)[1].lower()

        # 对文件名进行 Base64 编码
        encoded_filename = encode_filename(original_filename)

        # 使用 secure_filename 处理文件名
        filename = f"{encoded_filename}_{uuid.uuid4()}{file_extension}"

        # 创建保存路径
        image_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], f'{upload_type}/{type_id}')
        os.makedirs(image_folder, exist_ok=True)

        # 保存文件
        image_path = os.path.join(image_folder, filename)
        file.save(image_path)

        # 获取相对路径或 URL
        image_url = image_path

        return image_url
    else:
        return None
