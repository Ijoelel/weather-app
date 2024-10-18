import requests
import pandas as pd

url = "https://api.tomorrow.io/v4/weather/forecast?location=new%20york&apikey=AqwaRL5CVxt61JpyfxrCHeZAto4W6zlH"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

df = pd.DataFrame(response.text)

print(df)

# print(response.text)