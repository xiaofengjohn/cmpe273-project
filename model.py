from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand



# Database Configurations
app = Flask(__name__)
DATABASE = 'newtest'
PASSWORD = 'p@ssw0rd123'
USER = 'root'
HOSTNAME = 'mysqlserver'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)
db = SQLAlchemy(app)

# Database migration command line
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Location_API(db.Model):

	# Data Model Location api Table
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=False)
	address = db.Column(db.String(150), unique=False)
	city = db.Column(db.String(100), unique=False)
	state = db.Column(db.String(100), unique=False)
	zip = db.Column(db.String(100), unique=False)
	lat = db.Column(db.String(100), unique=False)
	lng = db.Column(db.String(100), unique=False)
	

	def __init__(self, name, address, city, state, zip, lat, lng):
		# initialize columns
		self.name = name
		self.address = address
		self.city = city
		self.state = state
		self.zip = zip
		self.lat = lat
		self.lng = lng
	
 
	def __repr__(self):
		return '<Location %r>' % self.name


class CreateDB():
	def __init__(self, hostname=None):
		if hostname != None:	
			HOSTNAME = hostname
		import sqlalchemy
		engine = sqlalchemy.create_engine('mysql://%s:%s@%s'%(USER, PASSWORD, HOSTNAME)) # connect to server
		engine.execute("CREATE DATABASE IF NOT EXISTS %s "%(DATABASE)) #create db

if __name__ == '__main__':
	manager.run()


