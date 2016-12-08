import requests, json
from requests.auth import HTTPBasicAuth

class lyft:
    """
    For Lyft object generation
    """
    def __init__(self):
        """
        initialize connection to the api url and get access token
        """
        self.client_id = 'ggWAbpJIjFfS'
        self.client_secret = '-8wIa_rQckhP4o0Ts0GfZJwEKrJaf2tc'
        self.token = self.__generate_token__()

        # define variables to be used in the request parameters
        token_val = 'Bearer '+self.token
        self.headers = {'Authorization':token_val}

    def __generate_token__(self):
        """
        use client_id and client_secret to generate access token.
        """
        url = 'https://api.lyft.com/oauth/token'

        # define request parameters
        payload = {"Content-Type": "application/json",
        "grant_type": "client_credentials",
        "scope": "public"}

        auth_header = HTTPBasicAuth(self.client_id, self.client_secret)

        # request data
        res = requests.post(url=url, data = payload,auth = auth_header)

        # extracting the token from the response
        token = res.json()['access_token']
        return token
    #For getting ride costs
    def lyft_price(self,start_lat,start_lng,end_lat,end_lng):
        """
         using the lyft cost api to get the prices for a route
        """
        url = 'https://api.lyft.com/v1/cost?start_lat='+str(start_lat)+'&start_lng='+str(start_lng)+'&end_lat='+str(end_lat)+'&end_lng='+str(end_lng)
        #data = json.loads(response.text)
        lyft_data = requests.get(url,headers=self.headers).json()['cost_estimates']
        for data in lyft_data:
            if data["ride_type"] == "lyft":
                price = float(data["estimated_cost_cents_min"]/100)

        return price
    
    #For getting distance travelled
    def lyft_distance(self,start_lat,start_lng,end_lat,end_lng):
        """
         using the lyft cost api to get the prices for a route
        """
        url = 'https://api.lyft.com/v1/cost?start_lat='+str(start_lat)+'&start_lng='+str(start_lng)+'&end_lat='+str(end_lat)+'&end_lng='+str(end_lng)
        #data = json.loads(response.text)
        lyft_data = requests.get(url,headers=self.headers).json()['cost_estimates']
        for data in lyft_data:
            if data["ride_type"] == "lyft":
                price = float(data["estimated_distance_miles"])

        return price
    
    #For getting ride duration
    def lyft_duration(self,start_lat,start_lng,end_lat,end_lng):
        """
         using the lyft cost api to get the prices for a route
        """
        url = 'https://api.lyft.com/v1/cost?start_lat='+str(start_lat)+'&start_lng='+str(start_lng)+'&end_lat='+str(end_lat)+'&end_lng='+str(end_lng)
        #data = json.loads(response.text)
        lyft_data = requests.get(url,headers=self.headers).json()['cost_estimates']
        #lyftPrices = []
        for data in lyft_data:
            if data["ride_type"] == "lyft":
                duration = float(data["estimated_duration_seconds"]/60)

        return duration
