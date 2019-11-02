from flask_sqlalchemy import SQLAlchemy
from wanghublog.extensions import bcrypt,cache
from flask import flash
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from itsdangerous import BadSignature, SignatureExpired
from uuid import uuid4
from flask_login import AnonymousUserMixin
from flask_principal import current_app

db = SQLAlchemy(use_native_unicode='utf8')

posts_tags = db.Table('posts_tags',
    db.Column('post_id', db.String(45), db.ForeignKey('posts.id')),
    db.Column('tag_id', db.String(45), db.ForeignKey('tags.id')))
users_roles = db.Table('users_roles',
    db.Column('user_id', db.String(45), db.ForeignKey('users.id')),
    db.Column('role_id', db.String(45), db.ForeignKey('roles.id')))
class User(db.Model):
    """Represents Proected users."""

    # Set the name for table
    __tablename__ = 'users'
    id = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    #one to many:User==>posts
    #Establish contact with Post's ForeignKey:user_id
    posts = db.relationship(
    	'Post',
    	backref='users',#backref：用于指定表之间的双向关系，如果在一对多的关系中建立双向的关系，这样的话在对方看来这就是一个多对一的关系
    	lazy='dynamic')#lazy：指定 SQLAlchemy 加载关联对象的方式,lazy=dynamic: 只有被使用时，对象才会被加载
    
    roles = db.relationship(
        'Role',
        secondary = users_roles,
        backref = db.backref('users',lazy='dynamic'))

    #def __init__(self, id, username, password):
        #self.id = id
        #self.username = username
        #self.password = self.set_password(password)
        # Setup the default-role for user.
        #default = Role.query.filter_by(name="default").one()
        #self.roles.append(default)

    def __repr__(self):
        """Define the string format for instance of User."""
        return "<Model User `{}`>".format(self.username)

    def set_password(self, password):#将密码转换为Bcrypt类型的哈希值
        """Convert the password to cryptograph via flask-bcrypt"""
        return bcrypt.generate_password_hash(password)

    def check_password(self, password):#检验输入密码的哈希值与数据库中密码的哈希值是否匹配
        return bcrypt.check_password_hash(self.password, password)

    def is_authenticated(self):
        """Check the user whether logged in."""

        # Check the User's instance whether Class AnonymousUserMixin's instance.
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active():#是否通过验证
        """Check the user whether pass the activation process."""

        return True

    def is_anonymous(self):#是否是匿名用户
        """Check the user's login status whether is anonymous."""

        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        """Get the user's uuid from database."""
        # selfid=self.id
        #return unicode(self.id)
        return str(self.id)

    @staticmethod
    @cache.memoize(60)
    def verify_auth_token(token):#验证token函数
        """Validate the token whether is night."""

        serializer = Serializer(
            current_app.config['SECRET_KEY'])
        try:
            # serializer object already has tokens in itself and wait for 
            # compare with token from HTTP Request /api/posts Method `POST`.
            data = serializer.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user = User.query.filter_by(id=data['id']).first()
        return user


class Post(db.Model):
    """Represents Proected posts."""
    __table_args__ = {
        'mysql_charset':'utf8'
    }
    __tablename__ = 'posts'
    id = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime)
    # Set the foreign key for Post
    user_id = db.Column(db.String(45), db.ForeignKey('users.id'))
    # Establish contact with Comment's ForeignKey: post_id
    comments = db.relationship(
        'Comment',
        backref='posts',
        lazy='dynamic')
    
    # many to many: posts <==> tags
    tags = db.relationship(
        'Tag',
        secondary=posts_tags,#seconddary(次级)：会告知 SQLAlchemy 该 many to many 的关联保存在 posts_tags 表中
        backref=db.backref('posts', lazy='dynamic'))#声明表之间的关系是双向

    def __init__(self):
        self.id = str(uuid4())

    def __repr__(self):
        return "<Model Post `{}`>".format(self.title)


class Tag(db.Model):
    """Represents Proected tags."""

    __tablename__ = 'tags'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self):
        self.id = str(uuid4())
        # self.name = name

    def __repr__(self):
        return "<Model Tag `{}`>".format(self.name)


class Comment(db.Model):
    """Represents Proected comments."""

    __tablename__ = 'comments'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.String(45), db.ForeignKey('posts.id'))

    def __init__(self):
        self.id = str(uuid4())
    def __repr__(self):
        return '<Model Comment `{}`>'.format(self.name)

class Role(db.Model):
    """Represents Proected roles."""
    __tablename__ = 'roles'

    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))

    def __init__(self):
        self.id = str(uuid4())


    def __repr__(self):
        return "<Model Role `{}`>".format(self.name)

class Reminder(db.Model):
    """Represents Proected reminders."""

    __tablename__ = 'reminders'
    id = db.Column(db.String(45), primary_key=True)
    date = db.Column(db.DateTime())
    email = db.Column(db.String(255))
    text = db.Column(db.Text())

    def __init__(self):
        self.id = str(uuid4())
        # self.email = email
        # self.text = text
        # self.date = datetime.now()
    def __repr__(self):
        return '<Model Reminder `{}`>'.format(self.text[:20])

