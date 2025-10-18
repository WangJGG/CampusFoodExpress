import os
import json
from repository.models import db  # Order 模型在 models.py 中定义
from repository.comment_repository import (
    add_comment_repository,
    delete_comment_repository,
    get_comment_by_id_repository,
    get_comment_and_restaurant_by_id_repository,
    get_comments_by_restaurant_repository,
    get_comments_by_user_repository,
    get_all_comments_repository,
    commit_changes
)
from common.utils import upload_images
from service.notification_service import NotificationService

def create_comment(user_id, data, files, host_url):
    """
    创建评论：
    - 检查 Order 是否存在
    - 检查 Order 是否已存在评论
    - 处理图片上传
    """
    # 将 rating 转换为整数（如有异常，则抛出异常）
    try:
        rating = int(data.get('rating'))
    except (ValueError, TypeError):
        raise Exception("Invalid rating value")
    
    try:
        # 处理图片上传
        image_paths = []
        if 'images' in files:
            file_list = files.getlist('images')
            for file in file_list:
                image_url = upload_images(file, user_id, upload_type="comments")
                if image_url:
                    image_paths.append(image_url)
                else:
                    raise Exception("图片上传失败")

        new_comment = add_comment_repository(user_id, data.get('order_id'), data.get('restaurant_id'), data.get('text'), rating, 
                                             ";".join(image_paths) if image_paths else None, str(data.get('is_anonymous', 'false')).lower() == 'true')

        # 发送订单通知
        NotificationService.create_notification(
            '评论已发布',
            '您的评论已发布，感谢您的支持。',
            user_id,
            data.get('order_id'),
            'Order Commented'
        )

        commit_changes()
        return new_comment, image_paths
    except Exception as e:
        db.session.rollback()
        raise e

def remove_comment(comment_id):
    """
    删除评论：
    - 删除评论前，获取关联 Order，并将 order.comment_id 置为 None
    - 删除评论时删除关联图片文件（如存在）
    - 发送系统通知告知评论作者
    """
    comment = get_comment_by_id_repository(comment_id)
    if comment is None:
        raise Exception("Comment not found")
    try:
        # 删除评论相关图片
        if comment.images:
            for image_path in comment.images.split(";"):
                if os.path.exists(image_path):
                    os.remove(image_path)

        delete_comment_repository(comment)

        # 发送系统通知
        NotificationService.create_notification(
            title="评论删除通知",
            content=f"您的评论（评论ID：{comment_id}）已被删除。",
            user_id=comment.user_id,
            type="Others"
        )
        commit_changes()
        return True
    except Exception as e:
        db.session.rollback()
        raise e


def get_comments_by_restaurant(restaurant_id, host_url):
    comments = get_comments_by_restaurant_repository(restaurant_id)
    comment_data = []
    for comment in comments:
        data = comment.to_dict()
        if comment.images:
            data['images'] = [f"{host_url}{img}" for img in comment.images.split(";")]
        comment_data.append(data)
    return comment_data

def get_comments_by_user(user_id):
    comments = get_comments_by_user_repository(user_id)
    comment_data = [
        {
            'id': comment.id,
            'restaurant_name': comment.restaurant_name,
            'rating': comment.rating,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for comment in comments
    ]
    return comment_data

def get_comment_detail(comment_id, host_url):
    comment_and_restaurant = get_comment_and_restaurant_by_id_repository(comment_id, host_url)
    return comment_and_restaurant

def get_all_comments(host_url):
    comments = get_all_comments_repository()
    comment_data = []
    for comment in comments:
        data = comment.to_dict()
        if comment.images:
            data['images'] = [f"{host_url}{img}" for img in comment.images.split(";")]
        comment_data.append(data)
    return comment_data
