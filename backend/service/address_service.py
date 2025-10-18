from repository.address_repository import add_address_repository, get_addresses_repository, delete_address_repository, commit_changes

def create_address(user_id, data):
    """
    根据传入数据构造 ShippingAddr 对象，并保存到数据库。
    此处可添加更多业务逻辑，例如数据校验或转换。
    """
    new_address = add_address_repository(user_id, data.get('contactName'), data.get('phone'), data.get('contactGender'), 
                           data.get('location'), data.get('tag'), data.get('lat'), data.get('lng'))
    commit_changes()
    return new_address

def get_addresses(user_id):
    """获取指定用户的所有地址。"""
    return get_addresses_repository(user_id)

def delete_address(address_id, user_id):
    """删除指定用户的地址，如果地址不存在则抛出异常。"""
    try:
        address = delete_address_repository(address_id, user_id)
        commit_changes()
        if not address:
            raise Exception("Address not found")
        return address
    except Exception as e:
        raise e
