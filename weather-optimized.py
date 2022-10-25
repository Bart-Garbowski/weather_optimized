import requests
import sys
from datetime import datetime
from datetime import timedelta
import os
import json
from io import StringIO
import csv

# klucz API do testøw: klucz wyslany oddzielnie
# Chester

api = sys.argv[1]

if len(sys.argv) > 2:
	requested_date = sys.argv[2]
else:
	requested_date = (datetime.today() + timedelta(days=1)).strftime("%m/%d/%Y")


class WeatherAPI:

	def __init__(self, klucz_api):
		self.klucz_api = klucz_api
		self.load_data()

	def items(self):
		for row in self.data.items():
			yield row

	def __iter__(self):
		return self.data.keys()

	def __getitem__(self, item):
		self.check_data(item)

	def get_data(self):
		url = "https://visual-crossing-weather.p.rapidapi.com/forecast"
		querystring = {"aggregateHours":"24","location":"Chester,UK","contentType":"csv","unitGroup":"us","shortColumnNames":"0"}
		headers = {
			"X-RapidAPI-Key": f"{self.klucz_api}",
			"X-RapidAPI-Host": "visual-crossing-weather.p.rapidapi.com"
		}
		response = requests.request("GET", url, headers=headers, params=querystring)

		f = StringIO(response.text)
		reader = csv.reader(f)

		weather = {}

		for idx, row in enumerate(reader):
			if idx == 0:
				continue
			dt = row[1]
			con = row[-1]
			weather[dt] = con

		self.data.update(weather)
		self.save_data()

	def load_data(self):
		if not os.path.exists("data.json"):
			self.data = {}
		else:
			with open("data.json") as file:
				self.data = json.load(file)

	def save_data(self):
		with open("data.json", mode="w") as file:
			json.dump(self.data, file)

	def check_data(self, requested_date):
		wth = self.data.get(requested_date)
		if not wth:
			self.get_data()
		wth = self.data.get(requested_date, "Wazne!, pogode mozna sprawdzic tylko "
											"na 14 dni do przodu, date wpisujemy w "
											"formacie mm/dd/rr ")


		if "Rain" in wth:
			print("Bedzie padac")
		elif "Sun" in wth:
			print("Nie bedzie padac")
		else:
			print("Nie wiem")


w = WeatherAPI(klucz_api=api)
w[requested_date]
print(w.items())
print(next(w.items()))
print(w.__iter__())

print(requested_date)
