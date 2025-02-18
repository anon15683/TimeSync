import requests
from dotenv import load_dotenv
import os

load_dotenv(override=True)

def get_data(from_date, to_date, session_id, auth_token, user_id, school_id):
    """
    Retrieves schedule data from the ALL4SCHOOLS API.

    This function sends a POST request to the ALL4SCHOOLS API to fetch schedule data
    for a specific student within a given date range.

    Parameters:
    from_date (str): The start date of the schedule period (format: 'YYYY-MM-DD').
    to_date (str): The end date of the schedule period (format: 'YYYY-MM-DD').
    session_id (str): The ASP.NET session ID for authentication.
    auth_token (str): The ASPXAUTH token for authentication.
    user_id (str): The ID of the student whose schedule is being requested.
    school_id (str): The ID of the school.

    Returns:
    dict or None: A dictionary containing the schedule data if the request is successful
                  and the response is in JSON format. Returns None if the request fails
                  or the response is not in JSON format.
    """
    base_url = os.getenv('ALL4SCHOOLS_URL')
    api_endpoint = 'api/api/Schedule/GetSchedule'
    full_url = f"{base_url}/{api_endpoint}"

    data = {
        "schoolId": school_id,
        "studentId": user_id,
        "from": from_date,
        "to": to_date,
        "getAbsences": False,
        "getShortNames": False
    }

    cookies = {
        "ASP.NET_SessionId": session_id,
        ".ASPXAUTH": auth_token
    }

    response = requests.post(full_url, json=data, cookies=cookies)

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
