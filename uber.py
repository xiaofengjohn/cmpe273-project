import requests
import json

url = 'https://api.uber.com/v1.2/estimates/price'
#Calling out the server for costs
def uber_price(start_lat, start_lng, end_lat, end_lng):
	parameters = {
	  'server_token': 'vsfheclyaHjkKaaKxdqlEABOB2IwXT0j6KoDP1FE',
	  'start_latitude': start_lat,
	  'start_longitude': start_lng,
	  'end_latitude': end_lat,
	  'end_longitude': end_lng,
	}
	response = requests.get(url, params=parameters)
	data = json.loads(response.text)

	for i in data["prices"]:
		if (i["localized_display_name"]== "uberX"):
			price = float(i["low_estimate"])
			distance = float(i["distance"])
	return price
#For distance 
def uber_distance(start_lat, start_lng, end_lat, end_lng):
	parameters = {
	  'server_token': 'vsfheclyaHjkKaaKxdqlEABOB2IwXT0j6KoDP1FE',
	  'start_latitude': start_lat,
	  'start_longitude': start_lng,
	  'end_latitude': end_lat,
	  'end_longitude': end_lng,
	}
	response = requests.get(url, params=parameters)
	data = json.loads(response.text)

	for i in data["prices"]:
		if (i["localized_display_name"]== "uberX"):
			price = float(i["low_estimate"])
			distance = float(i["distance"])
			duration = float(i["duration"]/60)

	return distance
#For ride duration
def uber_duration(start_lat, start_lng, end_lat, end_lng):
	parameters = {
	  'server_token': 'vsfheclyaHjkKaaKxdqlEABOB2IwXT0j6KoDP1FE',
	  'start_latitude': start_lat,
	  'start_longitude': start_lng,
	  'end_latitude': end_lat,
	  'end_longitude': end_lng,
	}
	response = requests.get(url, params=parameters)
	data = json.loads(response.text)

	for i in data["prices"]:
		if (i["localized_display_name"]== "uberX"):
			duration = float(i["duration"]/60)
	return duration
