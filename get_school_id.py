import os
from dotenv import load_dotenv
import requests

load_dotenv(override=True)

def get_school_id(session_id, auth_token):
    """
    Retrieves the school ID for the current user from the ALL4SCHOOLS API.

    This function makes a GET request to the ALL4SCHOOLS API to fetch the schools and settings
    for the current user. It then extracts and returns the ID of the first school in the response.

    Args:
        session_id (str): The ASP.NET session ID for authentication.
        auth_token (str): The ASPXAUTH token for authentication.

    Returns:
        str: The ID of the first school associated with the current user.

    Raises:
        requests.exceptions.HTTPError: If the API request fails or returns a non-200 status code.
    """
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
