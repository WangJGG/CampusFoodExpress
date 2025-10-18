from .models import Order, db, User, Restaurant
from datetime import datetime
# from repository.user_repository import get_user_by_id  # TODO
from repository.restaurant_repository import get_restaurant_by_id_repository
# 注意外键约束：检查user_id, restaurant_id, comment_id, delivery_person_id是否有效

def add_order_repository(order):
    """将新订单写入数据库。"""
    user = User.query.get(order.user_id)
    restaurant = get_restaurant_by_id_repository(order.restaurant_id)
    if not user or not restaurant:
        raise Exception("User or restaurant not found")
    db.session.add(order)

def get_all_orders_repository():
    """查询所有订单。"""
    return Order.query.all()

def get_order_by_id_repository(order_id):
    """根据订单 ID 查询订单。"""
    return Order.query.get(order_id)

def get_order_dict_by_id_repository(order_id):
    """根据订单 ID 查询订单字典, 包含用户、餐厅、配送员（可能没有）信息。"""
    order = get_order_by_id_repository(order_id)
    if not order:
        raise Exception("Order not found")
    
    user = User.query.get(order.user_id)
    restaurant = Restaurant.query.get(order.restaurant_id)
    if order.delivery_person_id is not None:
        delivery_person = User.query.get(order.delivery_person_id)
    order_dict = order.to_dict()
    order_dict['user'] = user.to_dict()
    order_dict['restaurant'] = restaurant.to_dict()
    if order.delivery_person_id is not None:
        order_dict['delivery_person'] = delivery_person.to_dict()
    return order_dict

def get_orders_by_user_repository(user_id):
    """根据用户 ID 查询订单。"""
    return Order.query.filter_by(user_id=user_id).all()

def get_orders_by_delivery_person_repository(delivery_person_id):
    """根据配送员 ID 查询订单。"""
    return Order.query.filter_by(delivery_person_id=delivery_person_id).all()

def get_orders_by_status_repository(status):
    """根据订单状态查询订单。"""
    return Order.query.filter_by(status=status).all()

def get_order_dict_by_status_repository(status):
    """根据订单状态查询订单字典, 包含用户、餐厅的信息。"""
    orders = get_orders_by_status_repository('Created')
    orders_created = []
    for order in orders:
        user = User.query.get(order.user_id)
        restaurant = Restaurant.query.get(order.restaurant_id)
        order_dict = order.to_dict()
        order_dict['user'] = user.to_dict() if user else None
        order_dict['restaurant'] = restaurant.to_dict() if restaurant else None
        orders_created.append(order_dict)
    return orders_created

def delete_order_repository(order):
    """标记订单为 Deleted 后提交。"""
    order.status = 'Deleted'

def commit_changes():
    """提交数据库更改。"""
    db.session.commit()