import requests
import csv
import pandas as pd


r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=asdfinterval=1min&apikey=TU10HCWDTV5CNVBN")
if r.status_code == 200:
	print("Hola")
else:
	print("la cagaste")
data = r.json()


dicto = []

for valor in data["Time Series (1min)"]:
	#print(data["Time Series (Daily)"][valor]["1. open"])
	d = data["Time Series (1min)"][valor]
	dicto.append(d)

#print(type(dicto))


#df= pd.DataFrame(dicto)
#print(df)
