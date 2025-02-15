import os
from dotenv import load_dotenv
import requests

load_dotenv(override=True)

def get_user_id(session_id, auth_token):
    """
    Retrieves the user ID from the ALL4SCHOOLS API using the provided session ID and authentication token.

    This function makes a GET request to the ALL4SCHOOLS API endpoint to fetch user information.
    It uses the session ID and authentication token for authorization.

    Args:
        session_id (str): The session ID for the current user session.
        auth_token (str): The authentication token for the current user.

    Returns:
        str: The user's CRM entity ID if the request is successful.

    Raises:
        requests.exceptions.HTTPError: If the API request fails or returns a non-200 status code.
    """
    base_url = os.getenv('ALL4SCHOOLS_URL')
    api_endpoint = 'api/Api/AppUser/GetUserInfo'
    full_url = f"{base_url}/{api_endpoint}"

    cookies = {
        "ASP.NET_SessionId": session_id,
        ".ASPXAUTH": auth_token
    }

    # Assuming you will use requests to make the API call
    response = requests.get(full_url, cookies=cookies)
    
    if response.status_code == 200:
        return response.json()["crmEntityId"]
    else:
        response.raise_for_status()
