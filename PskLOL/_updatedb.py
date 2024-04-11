import os 
import json 
import requests

# autoupdate the local database
url = "https://api.openalex.org/institutions"
# Get the directory of the current script
current_dir = os.path.dirname(__file__)
# Construct the path to the '_db' directory
db_dir = os.path.join(current_dir, '_db')
# Ensure the '_db' directory exists
os.makedirs(db_dir, exist_ok=True)
# Specify the path to the 'institute_db.json' file
institute_path = os.path.join(db_dir, 'institute_db.json')


def fetch_data(query:str):
    # Check if the request was successful
    params = {"search": query}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # Save the response content as JSON to a file
        if os.path.exists(institute_path): 
            with open(institute_path, "r") as file:
                data = json.load(file)
        else:
            data = {}
        data[query] = response.json()
        
        with open(institute_path, "w") as file:
            # file.write(response.text)
            json.dump(data, file)
        print("=====================================")
        print("Update Complete")
                
            
    else:
        print(f"Failed to fetch data: Status code {response.status_code}")
        
