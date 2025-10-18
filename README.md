# CampusFoodExpress - 校园食运通

## 📋 项目简介

CampusFoodExpress 是一个面向校园的综合性美食配送平台，集成了餐饮地图、顺手送、亲友互助等特色功能，为校园用户提供便捷的订餐和配送服务。

## 🚀 技术栈

### 前端技术
- **用户端 (frontend)**: Vue.js + Vue Router + Vuex
- **管理端 (frontend_admin)**: Vue.js + Element UI
- **地图服务**: 集成地图组件

### 后端技术
- **框架**: Flask (Python)
- **数据库**: SQLAlchemy ORM
- **Web服务器**: Gunicorn
- **认证**: JWT Token
- **实时通信**: WebSocket (聊天功能)

## 📁 项目结构

```
CampusFoodExpress/
├── frontend/              # 用户端前端（打包为移动端 APK）
│   ├── src/
│   │   ├── components/   # 公共组件
│   │   ├── views/        # 页面视图
│   │   ├── router/       # 路由配置
│   │   ├── service/      # API 服务层
│   │   └── utils/        # 工具函数
│   └── public/           # 静态资源
│
├── frontend_admin/        # 管理员端前端
│   ├── src/
│   │   ├── components/   # 管理端组件
│   │   ├── views/        # 管理页面
│   │   └── service/      # 管理端 API
│   └── public/
│
└── backend/              # 后端服务
    ├── common/           # 公共配置和工具
    │   ├── config.py     # 配置文件
    │   ├── decorators.py # 装饰器
    │   └── extensions.py # Flask 扩展
    ├── repository/       # 数据访问层
    │   ├── models.py     # 数据模型
    │   └── *_repository.py
    ├── service/          # 业务逻辑层
    │   └── *_service.py
    ├── routes/           # 路由控制层
    │   └── *.py
    ├── static/           # 静态文件存储
    │   └── uploads/      # 用户上传文件
    ├── test/             # 测试文件
    ├── app.py           # 应用入口
    └── wsgi.py          # WSGI 服务器配置
```

## ✨ 核心功能模块

### 1. 用户账号信息处理
- ✅ 用户注册与登录
- ✅ 账号安全退出
- ✅ 密码找回机制
- ✅ JWT Token 认证
- ✅ 用户实名认证

**相关文件:**
- `backend/routes/auth.py` - 认证路由
- `backend/service/auth_service.py` - 认证业务逻辑
- `backend/repository/auth_repository.py` - 认证数据访问

### 2. 管理员功能模块

#### 2.1 用户账号管理
- ✅ 用户列表查询
- ✅ 用户信息管理
- ✅ 账号状态控制
- ✅ 封禁/解封账号

#### 2.2 商家管理
- ✅ 商家入驻审核
- ✅ 实名制审批
- ✅ 商家信息管理

#### 2.3 举报与申诉处理
- ✅ 用户举报处理
- ✅ 举报内容审核
- ✅ 用户申诉受理
- ✅ 申诉结果反馈

**相关文件:**
- `backend/routes/admin.py` - 管理员路由
- `backend/service/admin_service.py` - 管理员服务
- `backend/service/report_service.py` - 举报处理服务
- `backend/repository/report_repository.py` - 举报数据管理

### 3. 顺手送功能 (Order)

校园特色功能，用户可以发布配送悬赏，其他用户接单配送。

- ✅ 发布配送悬赏
- ✅ 编辑悬赏信息
- ✅ 取消未接单悬赏
- ✅ 接受悬赏订单
- ✅ 配送员放弃订单
- ✅ 查询悬赏状态
- ✅ 确认送达
- ✅ 配送员联络
- ✅ 历史订单记录

**相关文件:**
- `backend/routes/order.py` - 订单路由
- `backend/service/order_service.py` - 订单业务逻辑
- `backend/repository/order_repository.py` - 订单数据管理
- `frontend/src/components/OrderList.vue` - 订单列表组件

### 4. 餐饮地图功能 (Restaurant)

基于地图的餐馆展示和查询功能。

- ✅ 地图显示餐馆位置
- ✅ 餐馆详细信息
- ✅ 餐馆简介展示
- ✅ 当前订单情况查询
- ✅ 商家评分系统
- ✅ 餐馆搜索功能
- ✅ 餐馆分类筛选

**相关文件:**
- `backend/routes/restaurant.py` - 餐馆路由
- `backend/service/restaurant_service.py` - 餐馆服务
- `backend/repository/restaurant_repository.py` - 餐馆数据
- `frontend/src/components/MapComponent.vue` - 地图组件
- `frontend/src/components/SearchBar.vue` - 搜索组件

### 5. 亲友互助功能 (Friends & Group)

社交化的用餐组队功能。

#### 5.1 亲友关系管理
- ✅ 添加亲友关系
- ✅ 解除亲友关系
- ✅ 亲友列表查看
- ✅ 亲友互助等级

#### 5.2 "干饭小群"功能
- ✅ 创建干饭小群
- ✅ 解散群组
- ✅ 加入小群
- ✅ 退出小群
- ✅ 群组聊天
- ✅ 群组管理（群主/管理员权限）
- ✅ 群成员管理

**相关文件:**
- `backend/routes/friends.py` - 好友路由
- `backend/service/friend_service.py` - 好友服务
- `backend/routes/eatinggroup.py` - 群组路由
- `backend/service/eatinggroup_service.py` - 群组服务
- `backend/routes/chat.py` - 聊天路由
- `backend/service/chat_service.py` - 聊天服务

### 6. 广播通知处理 (Notification)

多类型消息通知系统。

- ✅ 商家消息通知
- ✅ 系统消息通知
- ✅ 亲友消息通知
- ✅ 订单状态通知
- ✅ 通知浏览
- ✅ 删除通知
- ✅ 通知已读/未读状态

**相关文件:**
- `backend/routes/order_notification.py` - 通知路由
- `backend/service/notification_service.py` - 通知服务
- `backend/repository/notification_repository.py` - 通知数据

### 7. 个人信息管理 (User)

用户个性化设置和信息管理。

- ✅ 收藏餐馆
- ✅ 主页装饰
- ✅ 餐厅足迹记录
- ✅ 个人信息编辑
- ✅ 隐私设置
- ✅ 校园美食推荐笔记
- ✅ 密码修改
- ✅ 用户实名认证
- ✅ 用户状态展示

**相关文件:**
- `backend/routes/user.py` - 用户路由
- `backend/service/user_service.py` - 用户服务
- `backend/routes/favorite.py` - 收藏路由
- `backend/service/favorite_service.py` - 收藏服务
- `backend/routes/status.py` - 状态路由
- `backend/service/status_service.py` - 状态服务
- `backend/routes/comment.py` - 评论/笔记路由
- `backend/service/comment_service.py` - 评论服务
- `frontend/src/components/userStatus.vue` - 用户状态组件

### 8. 地址管理 (Address)

用户配送地址管理。

- ✅ 添加收货地址
- ✅ 编辑地址信息
- ✅ 删除地址
- ✅ 设置默认地址
- ✅ 地址列表查看

**相关文件:**
- `backend/routes/address.py` - 地址路由
- `backend/service/address_service.py` - 地址服务
- `backend/repository/address_repository.py` - 地址数据

## 🔧 安装与运行

### 前置要求
- Python 3.8+
- Node.js 14+
- SQLite 数据库


## 📝 API 文档

后端 API 遵循 RESTful 设计规范：

- **认证接口**: `/api/auth/*`
- **用户接口**: `/api/user/*`
- **订单接口**: `/api/order/*`
- **餐馆接口**: `/api/restaurant/*`
- **好友接口**: `/api/friends/*`
- **群组接口**: `/api/eatinggroup/*`
- **通知接口**: `/api/notification/*`
- **管理员接口**: `/api/admin/*`

详细 API 文档请参考各路由文件中的注释。

## 🔐 安全特性

- JWT Token 认证机制
- 密码加密存储
- CSRF 防护
- SQL 注入防护
- 文件上传安全检查
- 用户实名认证
- 账号封禁机制

## 📱 移动端支持

- 响应式设计，适配各种屏幕尺寸
- 支持打包为 Android APK

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 开源协议

本项目采用 [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) 开源协议。


## 👥 开发团队：造火箭施工队

- [Jack Wang](https://github.com/WangJGG)
- [TJU-YanJinghao](https://github.com/TJU-YanJinghao)
- [Zhu Yakun](https://github.com/Zhu-Yakun)
- [0-693](https://github.com/0-693)
- [yuehuarulian](https://github.com/yuehuarulian)
- [haojinw0027](https://github.com/haojinw0027)
- [Confident-Huangduer](https://github.com/Confident-Huangduer)





