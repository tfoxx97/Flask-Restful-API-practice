import requests
import json

BASE = "http://127.0.0.1:5000/"

test1_data = {"name": "chicken", "ingredients": {"1/2 cup": "flour"}, "instructions": "turn on heat for 400f."}
test2_data = {"name": "fish", "ingredients": {"1/2 cup": "soy sauce"}, "instructions": "turn on heat for 320f."}

response = requests.put(BASE + "recipes/1", 
                        data=json.dumps(test1_data), 
                        headers={'Content-Type': 'application/json'}
                    )
print(response.status_code, response.json())

response = requests.get(BASE)
print(response.status_code, response.json())