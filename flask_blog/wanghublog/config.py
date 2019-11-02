class Config(object):  
    """Base config class."""
    SECRET_KEY = '5cb42709c01449b2ca76e172e6ef4634'

class ProdConfig(Config):
    """Production config class."""
    pass

class DevConfig(Config):
    """Development config class."""
    # Open the DEBUG
    DEBUG = True
    # MySQL connection
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:125538@0.0.0.0:3306/test?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    """ RabbitMQ 使用默认的guest用户,端口为5672 """

    # Celery <--> RabbitMQ connection
    CELERY_RESULT_BACKEND = "amqp://guest:guest@localhost:5672//"
    CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"

    #### Flask-Cache's config
    CACHE_TYPE = 'simple'

    #### Flask-Assets's config
    # Can not compress the CSS/JS on Dev environment.开发环境中不打包，生产环境中自动打包
    ASSETS_DEBUG = True
