import caldav
import argparse

def list_icloud_calendars(username, app_specific_password):
    """
    List iCloud calendars for a given username and app-specific password.

    Args:
        username (str): The iCloud username.
        app_specific_password (str): The app-specific password for iCloud.

    Returns:
        None
    """
    # URL of the iCloud CalDAV server
    caldav_url = 'https://caldav.icloud.com/'

    # Connect to the iCloud CalDAV server
    client = caldav.DAVClient(url=caldav_url, username=username, password=app_specific_password)
    principal = client.principal()

    # Get the calendar
    calendars = principal.calendars()
    for calendar in calendars:
        print(f"Calendar Name: \033[94m{calendar.name}\033[0m\nURL: \033[92m{calendar.url}\033[0m\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List iCloud calendars.')
    parser.add_argument('-u', '--user', required=True, help='iCloud username')
    parser.add_argument('-p', '--password', required=True, help='iCloud app-specific password')

    args = parser.parse_args()
    list_icloud_calendars(args.user, args.password)