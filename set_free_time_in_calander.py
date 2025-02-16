from caldav import DAVClient
from datetime import datetime, timedelta
from icalendar import Event, Alarm
import uuid
from icalendar import Calendar
from dotenv import load_dotenv
import os
from dateutil.parser import parse

load_dotenv(override=True)

def remove_events_in_time_range(time_range):
    """
    Remove events from a SOGo calendar that fall within a specified time range.

    This function connects to a SOGo calendar, retrieves events within a certain date range,
    and deletes any events that overlap with the specified time range.

    Parameters:
    time_range (dict): A dictionary containing the start and end times for the range
                       in which events should be removed. It should have two keys:
                       'start' and 'end', with string values that can be parsed into
                       datetime objects.

    Returns:
    None

    Note:
    - This function relies on environment variables for calendar connection details.
    - It uses the caldav library to interact with the calendar.
    - Events are deleted if they start, end, or span within the specified time range.
    """
    url = os.getenv('SOGO_CALENDAR_URL')
    username = os.getenv('SOGO_USERNAME')
    password = os.getenv('SOGO_PASSWORD')

    client = DAVClient(url=url, username=username, password=password)
    calendar__ = client.calendar(url=os.getenv('SOGO_CALENDAR_URL'))

    start = datetime.now()
    end = datetime.now() + timedelta(days=int(os.getenv('DAYS_TO_UPDATE')))
    existing_events = calendar__.date_search(start, end)

    range_start = parse(time_range['start'])
    range_end = parse(time_range['end'])

    for event in existing_events:
        event_start = event.vobject_instance.vevent.dtstart.value
        event_end = event.vobject_instance.vevent.dtend.value

        if (event_start > range_start and event_start < range_end) or \
           (event_end > range_start and event_end < range_end) or \
           (event_start < range_start and event_end > range_end):
            event.delete()

