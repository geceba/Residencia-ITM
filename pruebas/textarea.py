from tkinter import *
import requests
import pandas as pd

from arima import ModeloArima as ar


r = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=1min&apikey=TU10HCWDTV5CNVBN")

data = r.json()
print(type(data))

dicto = []

for valor in data["Time Series (1min)"]:
	#print(data["Time Series (Daily)"][valor]["1. open"])
	d = data["Time Series (1min)"][valor]
	dicto.append(d)

print(type(dicto))


df= pd.DataFrame(dicto)
    # extract the columns you want
value = df['4. close'].astype(float)
af = ar.arima_modelo(value)

root = Tk()
S = Scrollbar(root)
T = Text(root, height=27, width=100)
S.pack(side=RIGHT, fill=Y)
T.pack(side=LEFT, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
quote = af
T.insert(END, quote)
mainloop(  )