from app import create_app
from repository.models import User, db

app = create_app()
with app.app_context():
    # 检查是否已存在管理员账号
    if not User.query.filter_by(phone='18790598665').first():
        # 创建管理员账号
        admin_user = User(
            nickname='Admin',
            phone='18790598665',
            bio='This is the admin account',
            is_admin=True,          # 设置为管理员
            is_forbidden=False       # 确保账号未被禁止
        )
        admin_user.set_password('18790598665')  # 设置管理员密码
        db.session.add(admin_user)
        db.session.commit()
        print("管理员账号创建成功！")
    else:
        print("管理员账号已存在。")
