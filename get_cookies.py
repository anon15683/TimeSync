import requests
from dotenv import load_dotenv
import os

load_dotenv(override=True)
def get_cookies():
    base_url = os.getenv('ALL4SCHOOLS_URL')
    api_endpoint = 'modules/Login.aspx'
    full_url = f"{base_url}/{api_endpoint}"

    data = {
        "__VIEWSTATE": os.getenv('ALL4SCHOOLS_VIEWSTATE'),
        "__EVENTVALIDATION": os.getenv('ALL4SCHOOLS_EVENTVALIDATION'),
        "loginbutton": "",
        "username": os.getenv('ALL4SCHOOLS_USERNAME'),
        "password": os.getenv('ALL4SCHOOLS_PASSWORD'),
    }

    response = requests.post(full_url, data=data, allow_redirects=False)

    cookies = response.headers.get("Set-Cookie")
    session_id = None
    auth_token = None

    if cookies:
        cookies_list = cookies.split(", ")
        for cookie in cookies_list:
            if cookie.startswith("ASP.NET_SessionId"):
                session_id = cookie.split(";")[0].split("=")[1]
            elif cookie.startswith(".ASPXAUTH"):
                auth_token = cookie.split(";")[0].split("=")[1]

    return session_id, auth_token