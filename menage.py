
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from info import con,db
from info import models
app = con('d')
manage = Manager(app)
Migrate(app,db)
manage.add_command('mysql',MigrateCommand)

if __name__ == '__main__':
    print(app.url_map)
    manage.run()
