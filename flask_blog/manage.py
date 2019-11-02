#import Flask Script object
from flask_script import Manager, Server
from flask_migrate import Migrate,MigrateCommand
from wanghublog import models,create_app
from flask_bootstrap import Bootstrap
import os
from flask_assets import ManageAssets
from wanghublog.extensions import assets_env


# Get the ENV from os_environ使用工厂模式生成app，使得程序自动适应不同运行环境
env = os.environ.get('BLOG_ENV', 'dev')
# Create thr app instance via Factory Method
app = create_app('wanghublog.config.%sConfig' % env.capitalize())
# Init manager object via app object
manager = Manager(app)
bootstrap = Bootstrap(app)
# Init migrate object via app and db object
migrate = Migrate(app, models.db)

# Create a new commands: server
# This command will be run the Flask development_env server
manager.add_command("server", Server())
manager.add_command("db", MigrateCommand)
manager.add_command('assets',ManageAssets(assets_env))

@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    # 确保有导入 Flask app object，否则启动的 CLI 上下文中仍然没有 app 对象
    return dict(app=app,
    			db=models.db,
                User=models.User,
                Post=models.Post,
                Comment=models.Comment,
                Tag=models.Tag,
                Role=models.Role,
                Reminder = models.Reminder)

if __name__ == '__main__':
    import pdb
    #pdb.set_trace()
    manager.run()
