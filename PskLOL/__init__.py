import json 
import requests

# autoupdate the local database
url = "https://api.openalex.org/institutions"
params = {"search": "carnegie mellon university"}

# Send the GET request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Save the response content as JSON to a file
    with open("./db/"+params["search"]+".json", "w") as file:
        file.write(response.text)
else:
    print(f"Failed to fetch data: Status code {response.status_code}")
