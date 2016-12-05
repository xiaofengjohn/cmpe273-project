import requests 

url = "https://maps.googleapis.com/maps/api/geocode/json?address="

def address_to_cordinate(address):
	address_url = url + address.replace(' ', '+')
	resposne = requests.get(address_url)
	Json_response = resposne.json()
	coordinates = Json_response['results'][0]['geometry']['location']
	return coordinates
