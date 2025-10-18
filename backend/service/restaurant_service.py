from repository.models import db
from repository.restaurant_repository import (
    add_restaurant_repository,
    delete_restaurant_repository,
    get_restaurant_by_id_repository,
    get_all_restaurants_repository,
    get_restaurants_by_name_repository,
    commit_changes
)
from common.utils import upload_images
import os

def create_restaurant(data, files, host_url):
    image_path = None
    qr_code_path = None

    # 上传图片（如有）
    if 'image' in files:
        file = files['image']
        image_path = upload_images(file, data['id'], upload_type="restaurants")
        if not image_path:
            raise Exception('图片上传失败')
    if 'qr_code' in files:
        file = files['qr_code']
        qr_code_path = upload_images(file, data['id'], upload_type="restaurants")
        if not qr_code_path:
            raise Exception('图片上传失败')

    new_restaurant = add_restaurant_repository(data['name'], data['address'], data['phone'], qr_code_path, data.get('is_forbidden', False), 
                              data.get('description'), data.get('sales', 0), image_path, float(data.get('lat', 0)), float(data.get('lng', 0)))
    commit_changes()

    # 返回给前端的响应数据：拼接完整 URL
    response = {
        'message': 'Restaurant added successfully',
        "qr_code": f"{host_url}{qr_code_path}" if qr_code_path else None,
        "image": f"{host_url}{image_path}" if image_path else None,
        "id": new_restaurant.id,
        "status": "forbid" if new_restaurant.is_forbidden else "normal"
    }
    return response

def update_restaurant(restaurant_id, data, files, host_url):
    restaurant = get_restaurant_by_id_repository(restaurant_id)
    if not restaurant:
        raise Exception("Restaurant not found")

    restaurant.name = data.get('name', restaurant.name)
    restaurant.address = data.get('address', restaurant.address)
    restaurant.phone = data.get('phone', restaurant.phone)
    restaurant.description = data.get('description', restaurant.description)
    restaurant.sales = data.get('sales', restaurant.sales)
    restaurant.lat = float(data.get('lat', restaurant.lat))
    restaurant.lng = float(data.get('lng', restaurant.lng))
    # 根据传入 status 更新 is_forbidden，默认判断 status 是否为 'normal'
    status = data.get('status')
    if status:
        restaurant.is_forbidden = False if status == 'normal' else True
    restaurant.rating = data.get('rating', restaurant.rating)

    # 如果有新的图片上传，则删除旧图并更新路径
    try:
        if 'image' in files:
            file = files['image']
            image_path = upload_images(file, restaurant_id, upload_type="restaurants")
            if not image_path:
                raise Exception('图片上传失败')
            if restaurant.image and os.path.exists(restaurant.image):
                os.remove(restaurant.image)
            restaurant.image = image_path

        if 'qr_code' in files:
            file = files['qr_code']
            qr_code_path = upload_images(file, restaurant_id, upload_type="restaurants")
            if not qr_code_path:
                raise Exception('图片上传失败')
            if restaurant.qr_code and os.path.exists(restaurant.qr_code):
                os.remove(restaurant.qr_code)
            restaurant.qr_code = qr_code_path

        commit_changes()

        qr_code_final = restaurant.qr_code if restaurant.qr_code else f"static/default/qr_code_default.png"
        image_final = restaurant.image if restaurant.image else f"static/default/restaurant_default.png"

        response = {
            'message': 'Restaurant updated successfully',
            "qr_code": f"{host_url}{qr_code_final}",
            "image": f"{host_url}{image_final}"
        }
        return response
    except Exception as e:
        raise Exception(str(e))

def remove_restaurant(restaurant_id):
    response = delete_restaurant_repository(restaurant_id)
    commit_changes()
    if 'error' in response:
        raise Exception(response['error'])
    return {'message': 'Restaurant deleted successfully'}

def forbid_restaurant(restaurant_id):
    restaurant = get_restaurant_by_id_repository(restaurant_id)
    if not restaurant:
        raise Exception("Restaurant not found")
    restaurant.is_forbidden = True
    commit_changes()
    return {'message': 'Restaurant forbidden successfully'}

def unforbid_restaurant(restaurant_id):
    restaurant = get_restaurant_by_id_repository(restaurant_id)
    if not restaurant:
        raise Exception("Restaurant not found")
    restaurant.is_forbidden = False
    commit_changes()
    return {'message': 'Restaurant unforbidden successfully'}

def get_all_unforbidden_restaurants(host_url):
    restaurants = get_all_restaurants_repository()
    restaurant_data = []
    for restaurant in restaurants:
        if restaurant.is_forbidden:
            continue
        data = restaurant.to_dict()
        data.pop('is_forbidden')
        data['status'] = 'normal'
        data['image'] = f"{host_url}{restaurant.image}" if restaurant.image else f"{host_url}static/default/restaurant_default.png"
        data['qr_code'] = f"{host_url}{restaurant.qr_code}" if restaurant.qr_code else f"{host_url}static/default/qr_code_default.png"
        restaurant_data.append(data)
    return restaurant_data

def get_all_restaurants(host_url):
    restaurants = get_all_restaurants_repository()
    restaurant_data = []
    for restaurant in restaurants:
        data = restaurant.to_dict()
        is_forbidden = data.pop('is_forbidden')
        data['status'] = 'forbided' if is_forbidden else 'normal'
        data['image'] = f"{host_url}{restaurant.image}" if restaurant.image else f"{host_url}static/default/restaurant_default.png"
        data['qr_code'] = f"{host_url}{restaurant.qr_code}" if restaurant.qr_code else f"{host_url}static/default/qr_code_default.png"
        restaurant_data.append(data)
    return restaurant_data

def get_restaurants_by_name(name, host_url):
    restaurants = get_restaurants_by_name_repository(name)
    restaurant_data = []
    for r in restaurants:
        data = r.to_dict()
        data['image'] = f"{host_url}{r.image}" if r.image else f"{host_url}static/default/restaurant_default.png"
        data['qr_code'] = f"{host_url}{r.qr_code}" if r.qr_code else f"{host_url}static/default/qr_code_default.png"
        restaurant_data.append(data)
    return restaurant_data

def get_restaurant_by_id(restaurant_id, host_url):
    restaurant = get_restaurant_by_id_repository(restaurant_id)
    if not restaurant:
        raise Exception("Restaurant not found")
    data = restaurant.to_dict()
    if restaurant.image:
        data['image'] = f"{host_url}{restaurant.image}"
    if restaurant.qr_code:
        data['qr_code'] = f"{host_url}{restaurant.qr_code}"
    return data

def get_restaurant_markers():
    # 如有需要可返回部分字段
    restaurants = get_all_restaurants_repository()
    return [r.to_dict() for r in restaurants]
