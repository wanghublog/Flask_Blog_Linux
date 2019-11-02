from flask import session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_principal import Principal,Permission,RoleNeed
from flask_oauthlib.client import OAuth
import os
from flask_celery import Celery
from flask_mail import Mail
from flask_cache import Cache
from flask_assets import Environment,Bundle
from flask_admin import Admin
from flask_restful import Api
#初始化对象
#Creat the Flask-Bcrypt's instabce
bcrypt = Bcrypt()
# Create the Flask-Celery-Helper's instance
flask_celery = Celery()
mail = Mail()

cache = Cache()
flask_admin = Admin()
restful_api = Api()
# Create the Flask-Login's instance
login_manager = LoginManager()
assets_env = Environment()
# Setup the configuration for login manager.
#     1. Set the login page.
#     2. Set the more stronger auth-protection.
#     3. Show the information when you are logging.
#     4. Set the Login Messages type as `information`.
login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"

# Create the Flask-Principal's instance
principals = Principal()

# 这里设定了 3 种权限, 这些权限会被绑定到 Identity 之后才会发挥作用.
# Init the role permission via RoleNeed(Need).
admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))


@login_manager.user_loader
def load_user(user_id):
    """Load the user's info."""
    from wanghublog.models import User
    return User.query.filter_by(id=user_id).first()

oauth = OAuth()
QQ_APP_ID = os.getenv('QQ_APP_ID', '101766182')
QQ_APP_KEY = os.getenv('QQ_APP_KEY', 'ec6587980aa6744a3633749531bb5855')
qq = oauth.remote_app(
    'qq',
    consumer_key=QQ_APP_ID,
    consumer_secret=QQ_APP_KEY,
    base_url='https://graph.qq.com/',
    request_token_url=None,
    request_token_params={'scope': 'blog.home'},
    access_token_url='/oauth2.0/token',
    authorize_url='/oauth2.0/authorize',
)

@qq.tokengetter
def get_qq_token():
    return session.get('qq_oauth_token')

# Define the set for js and css file.
main_css = Bundle(
    'css/bootstrap.css',
    'css/bootstrap-theme.css',
    filters='cssmin',
    output='assets/css/common.css')

main_js = Bundle(
    'js/bootstrap.js',
    filters='jsmin',
    output='assets/js/common.js')#output定义了打包后的包文件的存放路径
