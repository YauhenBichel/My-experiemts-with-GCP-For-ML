url = "https://us-central1-aiplatform.googleapis.com/v1beta1/projects/176050699085/locations/us-central1/endpoints/20248606137122816:predict"
import requests
import json
import google.auth
import google.auth.transport.requests

credentials, project_id = google.auth.default(
        scopes=['https://www.googleapis.com/auth/cloud-platform','https://www.googleapis.com/auth/cloud-platform.read-only'])

request = google.auth.transport.requests.Request()

credentials.refresh(request)

token = credentials.token
headers = {'Authorization': 'Bearer ' + token}
data = {
    "instances":
    [{
        "key":"value","key":"value"
    }]
} 

response = requests.post(url, json=data, headers=headers)

print(response.text)
print('------------------------------')
print(token)