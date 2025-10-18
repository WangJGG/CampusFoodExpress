from repository.order_repository import (
    add_order_repository,
    get_all_orders_repository,
    get_order_by_id_repository,
    get_order_dict_by_id_repository,
    get_orders_by_user_repository,
    get_orders_by_delivery_person_repository,
    get_order_dict_by_status_repository,
    delete_order_repository,
    commit_changes
)
from repository.models import Order
from datetime import datetime
from service.notification_service import NotificationService


def create_order(user_id, data):
    """
    根据请求数据构造 Order 对象，
    并进行时间转换、状态设置等处理后保存订单。
    """
    # 验证餐厅、送餐费、地址等由上层保证或在 Controller 中校验
    try:
        expected_pickup_time = datetime.fromisoformat(
            data.get('expected_pickup_time').replace('Z', '+00:00')
        ).astimezone()
        desired_delivery_time = datetime.fromisoformat(
            data.get('desired_delivery_time').replace('Z', '+00:00')
        ).astimezone()
    except Exception as e:
        raise Exception("Invalid time format") from e

    try:
        new_order = Order(
            restaurant_id=data.get('restaurant_id'),
            user_id=user_id,
            phone=data.get('phone'),
            gender=data.get('gender'),
            delivery_person_id=None,
            order_date=datetime.now(),
            expected_pickup_time=expected_pickup_time,
            desired_delivery_time=desired_delivery_time,
            status='Created',
            delivery_fee=data.get('delivery_fee'),
            completion_date=None,
            remarks=data.get('remarks'),
            address=data.get('address'),
            comment_id=None
        )
        add_order_repository(new_order)
        commit_changes()
        NotificationService.create_notification(title='新订单', content='您创建了一个新订单', user_id=new_order.user_id, order_id=new_order.id, type='Order Created')
        return new_order
    except Exception as e:
        raise Exception("Failed to create order") from e

def get_all_orders():
    return get_all_orders_repository()

def get_order_by_id(order_id):
    order_dict = get_order_dict_by_id_repository(order_id) # order user restaurant delivery_person
    return order_dict

def get_orders_by_user(user_id):
    return get_orders_by_user_repository(user_id)

def get_orders_by_delivery_person(delivery_person_id):
    return get_orders_by_delivery_person_repository(delivery_person_id)

def get_initiated_orders():
    """获取状态为 'Created' 的所有订单"""
    # 如有需要，可在此处补充关联查询（用户、餐厅等信息）
    orders_created = get_order_dict_by_status_repository('Created')
    return orders_created

def accept_order(order_id, delivery_person_id):
    order = get_order_by_id_repository(order_id)
    if not order:
        raise Exception("Order not found")
    if order.status != 'Created':
        raise Exception("Order has already been accepted")
    order.status = 'Shipped'
    order.delivery_person_id = delivery_person_id
    commit_changes()
    NotificationService.create_notification('订单已接单', '您的订单已在配送中', order.user_id, order.id, 'Order Shipped')
    NotificationService.create_notification('订单已接单', '您接受了一个新订单', delivery_person_id, order.id, 'Order Accepted')
    return order

def cancel_order(order_id):
    order = get_order_by_id_repository(order_id)
    if not order:
        raise Exception("Order not found")
    if order.status != 'Shipped':
        raise Exception("Order cannot be cancelled")
    order.status = 'Created'
    order.delivery_person_id = None
    commit_changes()
    NotificationService.create_notification('订单已取消', '您的订单已取消', order.user_id, order.id, 'Order Cancelled')
    return order

def complete_order(order_id):
    order = get_order_by_id_repository(order_id)
    if not order:
        raise Exception("Order not found")
    order.status = 'Completed'
    order.completion_date = datetime.now()
    commit_changes()
    NotificationService.create_notification('订单已完成', '您的订单已完成', order.user_id, order.id, 'Order Completed')
    return order

def delete_order(order_id):
    order = get_order_by_id_repository(order_id)
    if not order:
        raise Exception("Order not found")
    delete_order_repository(order)
    commit_changes()
    NotificationService.create_notification('订单已删除', '您的订单已删除', order.user_id, order.id, 'Order Deleted')
    return order
