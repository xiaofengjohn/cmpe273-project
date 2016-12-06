from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from model import db
from model import Location_API
from model import CreateDB
from model import app as application
import simplejson as json
from sqlalchemy.exc import IntegrityError
import os
import requests
import google_coordinates


app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template('index.html')

#adding a new location
@app.route('/locations', methods=['POST'])
def post():
	try:
		data = json.loads(request.data)
		if not data or not 'city' in data:
			abort(404)
		database = CreateDB(hostname = 'localhost')
		db.create_all()
		coordinate = google_coordinates.address_to_cordinate(data['address'] + data['city'] + data['state'] + data['zip'])
		lat = str(coordinate['lat'])
		lng = str(coordinate['lng'])
		new_location = Location_API(data['name'], data['address'], data['city'], data['state'], data['zip'], lat, lng)
		db.session.add(new_location)
		db.session.commit()
		added_location = {'id': new_location.id, 'name': new_location.name, 'address': new_location.address, 'city': new_location.city, 'state': new_location.state, 'zip': new_location.zip, 'coordinate': {'lat': new_location.lat, 'lng':new_location.lng}}
		return json.dumps(added_location), 201

	except IntegrityError:
		return json.dumps({'status':False})


@app.route('/locations/<location_id>',methods =['GET'])
def get_locationID(location_id):
	try:
		location = Location_API.query.filter_by(id=location_id).first_or_404()
		return json.dumps({'id': location.id, 'name': location.name, 'address': location.address, 'city': location.city, 'state': location.state, 'zip': location.zip, 'coordinate': {'lat': location.lat, 'lng':location.lng}})
	except IntegrityError:
		return json.dumps({'status':False})

@app.route('/locations/<location_id>',methods=['PUT'])
def update_locationID(location_id):
	try:
		location_data = json.loads(request.data)
		if location_data != None:
			new_name = location_data['name']
			location = Location_API.query.filter_by(id=location_id).first_or_404()
			location.name = new_name
			db.session.commit()
			return json.dumps("Accepted"),202
		else:
			return json.dumps("Error"),400

	except IntegrityError:
		return json.dumps({'status':False})

@app.route('/locations/<location_id>',methods=['DELETE'])
def delete_location(location_id):
	db.session.delete(Location_API.query.get(location_id))
        db.session.commit()
        return json.dumps({}),204


@app.route('/createdb')
def createDatabase():
	HOSTNAME = 'localhost'
	try:
		HOSTNAME = request.args['hostname']
	except:
		pass
	database = CreateDB(hostname = HOSTNAME)
	return json.dumps({'status':True})

@app.route('/info')
def app_status():
	return json.dumps({'server_info':application.config['SQLALCHEMY_DATABASE_URI']})

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5010, debug=True)
