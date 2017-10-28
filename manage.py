from flask_script import Manager
from flask_migrate import  MigrateCommand,Migrate
from zlktqa import app
from exts import db
from models import User,Question

manage = Manager(app)

# 使用migrate　绑定app, db
migrate = Migrate(app,db)
# 添加MigrteCommand 所有命令,迁移脚本的命令，init migrate,upgrade ,etc
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manage.run()