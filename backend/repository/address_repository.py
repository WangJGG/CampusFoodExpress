from .models import ShippingAddr, db, User
# 假设有一个用户 repository 或函数用于验证用户是否存在
# from routes.user import get_user_by_id  # TODO

def add_address_repository(user_id, name, phone, gender, location, tag, lat, lng):
    """将新地址写入数据库之前，先验证用户是否存在。"""
    # 模拟外键约束：检查 user_id
    user = User.query.filter_by(id=user_id).first()
    if not user:
        raise Exception("User not found")
    new_address = ShippingAddr(
        user_id=user_id,
        name=name,
        phone=phone,
        gender=gender,
        location=location,
        tag=tag,
        lat=lat,
        lng=lng
    )
    db.session.add(new_address)
    return new_address

def get_addresses_repository(user_id):
    """根据用户 ID 查询所有地址。"""
    return ShippingAddr.query.filter_by(user_id=user_id).all()

def delete_address_repository(address_id, user_id):
    """根据地址 ID 与用户 ID 删除地址记录。"""
    address = ShippingAddr.query.filter_by(id=address_id, user_id=user_id).first()
    if address:
        db.session.delete(address)
    return address

def commit_changes():
    """提交数据库更改。"""
    db.session.commit()