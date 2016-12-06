import requests
import json

#url = 'https://sandbox-api.uber.com/v1.2/estimates/price'
url = 'https://api.uber.com/v1.2/estimates/price'

start_lat = 21.3088619
start_lng = -157.8086674
end_lat = 21.2965912
end_lng =  -157.8564657


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
	#print json.dumps(data)
	for i in data["prices"]:
		if (i["localized_display_name"]== "uberX"):
			price = float(i["low_estimate"])
	return price

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
	#print json.dumps(data)
	for i in data["prices"]:
		if (i["localized_display_name"]== "uberX"):
			price = float(i["low_estimate"])
			distance = float(i["distance"])
			duration = float(i["duration"]/60)

	return distance
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
	#print json.dumps(data)
	for i in data["prices"]:
		if (i["localized_display_name"]== "uberX"):
			duration = float(i["duration"]/60)
	return duration
x = uber_price(start_lat, start_lng, end_lat, end_lng)
print x