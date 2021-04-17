from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '0331'
app.config['MYSQL_DATABASE_DB'] = 'learning'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)