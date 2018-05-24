from flask import session
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from info import con,db
app = con('e')
manage = Manager(app)
Migrate(app,db)
manage.add_command('mysql',MigrateCommand)

@app.route('/')
def index():
    session['name'] = 'qsj'
    return "index"

if __name__ == '__main__':
    manage.run()