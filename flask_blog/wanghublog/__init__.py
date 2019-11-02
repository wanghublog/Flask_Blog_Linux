from flask import Flask, redirect, url_for
#from wanghublog.config import DevConfig
from wanghublog.controllers import blog, main, admin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from wanghublog.extensions import bcrypt, login_manager, principals, flask_celery, mail, cache, assets_env, main_js, main_css, flask_admin,restful_api
from flask_principal import UserNeed, RoleNeed, identity_loaded
from flask_login import login_required, current_user
from wanghublog.models import User, Post, Role, Tag, Comment, Reminder
from wanghublog.tasks import on_reminder_save
from wanghublog.controllers.admin import CustomView, CustomModelView, PostView, CustomFileAdmin
from wanghublog.controllers.flask_restful.posts import PostApi
from wanghublog.controllers.flask_restful.auth import AuthApi
import os
def create_app(object_name):
    """Create the app instance via `Factory Method`"""
    app = Flask(__name__)
    # Will be load the SQLALCHEMY_DATABASE_URL from config.py to db object

    # Get the config from object of DecConfig
    # 使用 onfig.from_object() 而不使用 app.config['DEBUG'] 是因为这样可以加载 class DevConfig 的配置变量集合，而不需要一项一项的添加和修改。
    app.config.from_object(object_name)

    db = SQLAlchemy(app,use_native_unicode='utf8')


    db.init_app(app)
    # INIT the sqlalchemy object                            
    # Will be load the SQLALCHEMY_DATABASE_URL from config.py
    # SQLAlchemy 会自动的从 app 对象中的 DevConfig 中加载连接数据库的配置项
    
    # Init the Flask-Bcrypt via app object
    bcrypt.init_app(app)
    # Init the Flask-Login via app object
    login_manager.init_app(app)
    principals.init_app(app)
    
    flask_admin.init_app(app)
    flask_admin.add_view(CustomView(name='Custom'))
    flask_admin.add_view(PostView(Post,db.session,name='Post'))
    # Register view function `CustomModelView` into Flask-Admin
    models = [Role, Tag, Reminder, Comment]
    for model in models:
        flask_admin.add_view(
            CustomModelView(model, db.session, category='Models'))
    flask_admin.add_view(
        admin.CustomFileAdmin(
            os.path.join(os.path.dirname(__file__), 'static'),
            '/static',
            name='Static Files'))

    # Init the Flask-Celery-Helper via app object
    # Register the celery object into app object
    flask_celery.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    assets_env.init_app(app)
    assets_env.register('main_js',main_js)
    assets_env.register('main_css',main_css)

    # Define the route of restful_api
    restful_api.add_resource(
        PostApi,
        '/api/posts',
        '/api/posts/<string:post_id>',#表示可以访问 posts 这一类资源中某一个 post_id 一致的资源对象.
        endpoint='restful_api_post')
    restful_api.add_resource(
        AuthApi,
        '/api/auth',
        endpoint='restful_api_auth')
    restful_api.init_app(app)
    
    # 指定 URL='/' 的路由规则
    # 当访问 HTTP://server_ip/ GET(Default) 时，call home()
    @app.route('/')
    def index():
        # Redirect the Request_url '/' to '/blog/'
        return redirect(url_for('blog.home'))

   
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        """Change the role via add the Need object into Role.
            #设置当前用户身份为login登录对象
           Need the access the app object.
        """

        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity user object
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add each role to the identity user object
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    # Will be callback on_reminder_save when insert recond into table `reminder`.
    event.listen(Reminder, 'after_insert', on_reminder_save)
    from .api import bp
    app.register_blueprint(bp)
    
    # Register the Blueprint into app object
    app.register_blueprint(blog.blog_blueprint)
    app.register_blueprint(main.main_blueprint)

    return app
    


'''
if __name__ == '__main__':
    # Entry the application 
    app.run()
'''
