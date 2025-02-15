import os
from dotenv import load_dotenv
import requests

load_dotenv(override=True)

def get_school_id(session_id, auth_token):
    base_url = os.getenv('ALL4SCHOOLS_URL')
    api_endpoint = 'api/Api/AppUser/GetSchoolsAndSettingsForCurrentUser'
    full_url = f"{base_url}/{api_endpoint}"

    cookies = {
        "ASP.NET_SessionId": session_id,
        ".ASPXAUTH": auth_token
    }

    # Assuming you will use requests to make the API call
    response = requests.get(full_url, cookies=cookies)
    
    if response.status_code == 200:
        return response.json()[0]["id"]
    else:
        response.raise_for_status()