""" backend project setup """
from flask import Flask
from common.config import Config
from common.extensions import db, bcrypt, jwt, socketio
from routes.user import user_bp
from routes.admin import admin_bp
from routes.restaurant import restaurant_bp
from routes.order import order_bp
from routes.report import report_bp
from routes.favorite import favorite_bp
from routes.auth import auth_bp
from routes.status import status_bp
from routes.comment import comment_bp
from routes.system import system_notification_bp#, init_
from routes.order_notification import order_notification_bp
from routes.eatinggroup import eatinggroup_bp
from routes.friends import friend_bp
from routes.chat import chat_bp
from routes.address import address_bp
from flask_cors import CORS
# from models import Restaurant, User, Order# group_init


def create_app():
    """backend project creation
    
    returns: app object
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register Blueprints
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(restaurant_bp, url_prefix='/api/restaurant')
    app.register_blueprint(order_bp, url_prefix='/api/order')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    app.register_blueprint(favorite_bp, url_prefix='/api/favorite')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(status_bp, url_prefix='/api/status')
    app.register_blueprint(comment_bp, url_prefix='/api/comment')
    app.register_blueprint(friend_bp, url_prefix='/api/friend')
    app.register_blueprint(system_notification_bp, url_prefix='/api/system_notification')
    app.register_blueprint(order_notification_bp, url_prefix='/api/order_notification')
    app.register_blueprint(eatinggroup_bp, url_prefix='/api/eatinggroup')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(address_bp, url_prefix='/api/address')
    with app.app_context():
        db.create_all()
        # group_init()
        # User.init()
        # Restaurant.init()
        # Order.init()
        # init_()

    CORS(app, resources={r"/*": {"origins": ["http://localhost:8080","http://localhost:8081"]}},supports_credentials=True)
    # CORS(app, resources={r"/*": {"origins": "http://100.78.9.135:8080"}}, supports_credentials=True)
    return app
