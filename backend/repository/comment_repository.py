from .models import Comment, db
from .models import Restaurant, User, Order
# from repository.user_repository import get_user_by_id  # TODO
from datetime import datetime, timezone
from repository.restaurant_repository import get_restaurant_by_id_repository
from repository.order_repository import get_order_by_id_repository

def add_comment_repository(user_id, order_id, restaurant_id, text, rating, images, is_anonymous):
    """将新评论写入数据库。"""
    # 检查外键约束 User, Restaurant, Order, Comment
    user = User.query.get(user_id)
    if not user:
        raise Exception("User not found")
    
    restaurant = get_restaurant_by_id_repository(restaurant_id)
    if not restaurant:
        raise Exception("Restaurant not found")
    
    order = get_order_by_id_repository(order_id)
    if order is None:
        raise Exception("Order not found")
    if getattr(order, 'comment_id', None):
        raise Exception("Comment already exists for this order")

    new_comment = Comment(
        user_id=user_id,
        order_id=order_id,
        restaurant_id=restaurant_id,
        text=text,
        rating=rating,
        created_at=datetime.now(),
        images=images,
        is_anonymous = is_anonymous
    )
    db.session.add(new_comment)
    db.session.commit()
    order.comment_id = new_comment.id
    return new_comment

def delete_comment_repository(comment):
    """删除评论并提交。"""
    # 获取关联 order，并清空 comment_id
    order = Order.query.get(comment.order_id)
    if order:
        order.comment_id = None
    db.session.delete(comment)

def get_comment_by_id_repository(comment_id):
    """根据评论 ID 查询评论。"""
    return Comment.query.get(comment_id)

def get_comment_and_restaurant_by_id_repository(comment_id, host_url):
    """根据评论 ID 查询评论及关联餐厅信息。"""
    comment = get_comment_by_id_repository(comment_id)
    if comment is None:
        raise Exception("Comment not found")
    comment_and_restaurant = comment.to_dict()
    restaurant = Restaurant.query.get(comment.restaurant_id)
    if restaurant:
        comment_and_restaurant['restaurant_name'] = restaurant.name
        comment_and_restaurant['restaurant_image'] = f"{host_url}{restaurant.image}" if restaurant.image else None
        comment_and_restaurant['restaurant_rating'] = restaurant.rating
    if comment.images:
        comment_and_restaurant['images'] = [f"{host_url}{img}" for img in comment.images.split(";")]
    return comment_and_restaurant

def get_comments_by_restaurant_repository(restaurant_id):
    """根据餐厅 ID 查询评论。"""
    return Comment.query.filter_by(restaurant_id=restaurant_id).all()

def get_comments_by_user_repository(user_id):
    """根据用户 ID 查询评论。"""
    # 此处构造更丰富的数据，关联餐厅名称等（需要额外查询 Restaurant 表）
    comments = db.session.query(
        Comment.id,
        Comment.rating,
        Comment.created_at,
        Restaurant.name.label('restaurant_name')
    ).join(Restaurant, Comment.restaurant_id == Restaurant.id).filter(Comment.user_id == user_id).all()
    return comments

def get_all_comments_repository():
    """查询所有评论。"""
    return Comment.query.all()

def commit_changes():
    """提交数据库更改。"""
    db.session.commit()
