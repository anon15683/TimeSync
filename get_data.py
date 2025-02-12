import requests
from dotenv import load_dotenv
import os

load_dotenv(override=True)

def get_data(from_date, to_date, session_id, auth_token):
    url = os.getenv('ALL4SCHOOLS_API_URL')
    
    data = {
        "schoolId": 35,
        "studentId": 4707,
        "from": from_date,
        "to": to_date,
        "getAbsences": False,
        "getShortNames": False
    }

    cookies = {
        "ASP.NET_SessionId": session_id,
        ".ASPXAUTH": auth_token
    }

    response = requests.post(url, json=data, cookies=cookies)

    if response.status_code == 200:
        try:
            data = response.json()
            return data
        except requests.exceptions.JSONDecodeError:
            print("Response content is not in JSON format")
            return None
    else:
        print(f"Request failed with status code {response.status_code}")
        return None