from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from sqlalchemy import desc
from model import db
from model import Location_API
from model import CreateDB
from model import app as application
import simplejson as json
from sqlalchemy.exc import IntegrityError
import os
import requests
import google_coordinates
import json
import uber
from lyft import lyft
from tsp import TSP
#import Trips
lyft = lyft()

app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template('index.html')

#find all locations
@app.route('/locations',methods =['GET'])
def findAll():
	try:
		locations = Location_API.query.order_by(desc(Location_API.id)).all();
		result = [];
		for location in locations:
			result.append({'id': location.id, 'name': location.name, 'address': location.address, 'city': location.city, 'state': location.state, 'zip': location.zip, 'coordinate': {'lat': location.lat, 'lng':location.lng}});
		return json.dumps(result), 201;
	except IntegrityError:
		return json.dumps({'status':False})


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

@app.route('/trips', methods=['POST'])
def trip_estimator():
	#lyft = lyft()
	global lyft
	data1 = json.loads(request.data)
	startID = data1['start']
	locationsID = data1['others']


	alllocations=[]
	alllocations.append(int(startID))
	for i in range(len(locationsID)):
		alllocations.append(int(locationsID[i]))
	#print alllocations

	#start_location = Location_API.query.filter_by(id=start).first_or_404()
	#alllocations.append(start_location.id)
	#end_location = Location_API.query.filter_by(id=start).first_or_404()

	#create a dictionary for mapping the matrix numbers to the locatcation ids
	location = []
	for i in range(len(alllocations)):
		location.append(Location_API.query.filter_by(id=alllocations[i]).first_or_404())
		#print location[i]
		#print location[i].lat
		#alllocations.append(location[i].id)

	matrixlength = len(alllocations)
	Ubermatrix=[[0 for row in range(0,matrixlength)] for col in range(0,matrixlength)]
	for i in range(matrixlength):
		for j in range(matrixlength):
			if i == j:
				Ubermatrix[i][j] = 0
			else:
				Ubermatrix[i][j]= uber.uber_price(location[i].lat, location[i].lng, location[j].lat, location[j].lng)
	        #print Ubermatrix[i][j]

	#x = uber.uber_price(location[0].lat, location[0].lng, location[0].lat, location[0].lng)
	#print x
	#lyft = lyft()
	lyftmatrix=[[0 for row in range(0,matrixlength)] for col in range(0,matrixlength)]
	for i in range(matrixlength):
		for j in range(matrixlength):
			if i == j:
				lyftmatrix[i][j] = 0
			else:
				lyftmatrix[i][j]= lyft.lyft_price(location[i].lat, location[i].lng, location[j].lat, location[j].lng)
	        #print lyftmatrix[i][j]
	#for i in range(matrixlength):
	#	for j in range(matrixlength):
	#		print Ubermatrix[i][j]
	bestroute_uber = TSP(Ubermatrix).getFinalCityFlow()
	bestroute_lyft = TSP(lyftmatrix).getFinalCityFlow()

	#print bestroute_uber
	#print bestroute_lyft

	Uber_bestroute_prices = []
	Uber_bestroute_distance = []
	Uber_bestroute_duration = []

	uber_best_route = bestroute_uber.split('->')
	#print uber_best_route
	uber_best_route_locations = []
	for i in range(0,len(uber_best_route)-1):
		#print uber_best_route[i]
		uber_best_route_locations.append(str(location[int(uber_best_route[i])].name))
		Uber_bestroute_prices.append(uber.uber_price(location[int(uber_best_route[i])].lat, location[int(uber_best_route[i])].lng, location[int(uber_best_route[i+1])].lat, location[int(uber_best_route[i+1])].lng))
		Uber_bestroute_distance.append(uber.uber_distance(location[int(uber_best_route[i])].lat, location[int(uber_best_route[i])].lng, location[int(uber_best_route[i+1])].lat, location[int(uber_best_route[i+1])].lng))
		Uber_bestroute_duration.append(uber.uber_duration(location[int(uber_best_route[i])].lat, location[int(uber_best_route[i])].lng, location[int(uber_best_route[i+1])].lat, location[int(uber_best_route[i+1])].lng))

	#print Uber_bestroute_prices      
	uber_price_total = sum(Uber_bestroute_prices)
	uber_distance_total = sum(Uber_bestroute_distance)
	uber_duration_total = sum(Uber_bestroute_duration)
	#print uber_price_total

	lyft_bestroute_prices = []
	lyft_bestroute_distance = []
	lyft_bestroute_duration = []

	lyft_best_route = bestroute_lyft.split('->')
	#print lyft_best_route
	lyft_best_route_locations = []
	for i in range(0,len(lyft_best_route)-1):
		#print lyft_best_route[i]
		lyft_best_route_locations.append(str(location[int(lyft_best_route[i])].name))
		lyft_bestroute_prices.append(lyft.lyft_price(location[int(lyft_best_route[i])].lat, location[int(lyft_best_route[i])].lng, location[int(lyft_best_route[i+1])].lat, location[int(lyft_best_route[i+1])].lng))
		lyft_bestroute_distance.append(lyft.lyft_distance(location[int(lyft_best_route[i])].lat, location[int(lyft_best_route[i])].lng, location[int(lyft_best_route[i+1])].lat, location[int(lyft_best_route[i+1])].lng))
		lyft_bestroute_duration.append(lyft.lyft_duration(location[int(lyft_best_route[i])].lat, location[int(lyft_best_route[i])].lng, location[int(lyft_best_route[i+1])].lat, location[int(lyft_best_route[i+1])].lng))

	#print lyft_bestroute_prices      

	lyft_price_total = sum(lyft_bestroute_prices)
	lyft_distance_total = sum(lyft_bestroute_distance)
	lyft_duration_total = sum(lyft_bestroute_duration)
	#print lyft_price_total

	# "best_route_by_costs"

	uber_best_route_locations.pop(0)
	lyft_best_route_locations.pop(0)
	if lyft_price_total < uber_price_total:
		best_route_by_costs = lyft_best_route_locations
		start_location = str(location[int(lyft_best_route[0])].name)
	else:
		best_route_by_costs = lyft_best_route_locations
		start_location = str(location[int(uber_best_route[0])].name)
	#print best_route_by_costs

	#"providers"

	providers = []

	uber_response = {"name" : "Uber","total_costs_by_cheapest_car_type" : uber_price_total, "currency_code": "USD", "total_duration" : uber_duration_total, "duration_unit": "minute",  "total_distance" : uber_distance_total, "distance_unit": "mile"}
	lyft_response = {"name" : "Lyft","total_costs_by_cheapest_car_type" : lyft_price_total, "currency_code": "USD", "total_duration" : lyft_duration_total, "duration_unit": "minute",  "total_distance" : lyft_distance_total, "distance_unit": "mile"}
	 
	providers.append(uber_response)
	providers.append(lyft_response)

	trip_planner_response = {"start" : start_location, "best_route_by_costs" : best_route_by_costs, "providers" : providers, "end" : start_location}
	return json.dumps(trip_planner_response)








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
	app.run(host="0.0.0.0", port=5015, debug=False)

