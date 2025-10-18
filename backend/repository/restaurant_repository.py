from .models import Restaurant, db
from .models import Order, Comment, Favorite,Notification
import os

def add_restaurant_repository(name, address, phone, qr_code, is_forbidden, description, sales, image, lat, lng):
    new_restaurant = Restaurant(
        name = name,
        address = address,
        phone = phone,
        qr_code = qr_code,
        is_forbidden = is_forbidden,
        description = description,
        sales = sales,
        image = image,
        lat = lat,
        lng = lng,
    )
    db.session.add(new_restaurant)
    return new_restaurant

def delete_restaurant_repository(restaurant_id):
    restaurant = get_restaurant_by_id_repository(restaurant_id)
    if not restaurant:
        return {'error': 'Restaurant not found'}
    try:
        # 删除图片文件及所在目录（如存在）
        if restaurant.image and os.path.exists(restaurant.image):
            os.remove(restaurant.image)
            parent = os.path.dirname(restaurant.image)
            if os.path.exists(parent):
                for file in os.listdir(parent):
                    os.remove(os.path.join(parent, file))
                os.rmdir(parent)
        if restaurant.qr_code and os.path.exists(restaurant.qr_code):
            os.remove(restaurant.qr_code)
            parent = os.path.dirname(restaurant.qr_code)
            if os.path.exists(parent):
                for file in os.listdir(parent):
                    os.remove(os.path.join(parent, file))
                os.rmdir(parent)
        # 删除相关订单、评论、收藏等
        orders=Order.query.filter_by(restaurant_id=restaurant_id)
        comments=Comment.query.filter_by(restaurant_id=restaurant_id)
        favorites=Favorite.query.filter_by(restaurant_id=restaurant_id)
        for order in orders:
            Notification.query.filter_by(order_id=order.id).delete()
            db.session.delete(order)
        for comment in comments:
            db.session.delete(comment)
        for favorite in favorites:
            db.session.delete(favorite)
        db.session.delete(restaurant)
        return {'message': 'Restaurant deleted successfully'}
    except Exception as e:
        return {'error': str(e)}

def get_restaurant_by_id_repository(restaurant_id):
    return Restaurant.query.get(restaurant_id)

def get_all_restaurants_repository():
    return Restaurant.query.all()

def get_restaurants_by_name_repository(name):
    return Restaurant.query.filter_by(name=name).all()

def commit_changes():
    """提交数据库更改。"""
    db.session.commit()