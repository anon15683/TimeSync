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
    Remove events from a calendar that do not overlap with specified free time slots.

    This function connects to a calendar service, retrieves events within a specified date range,
    and deletes events that do not overlap with the provided free time slots.

    Parameters:
    time_range (list of dict): A list of dictionaries, where each dictionary represents a free time slot
                               with 'start' and 'end' keys containing datetime strings.

    Returns:
    None

    Note:
    - The function uses environment variables for calendar service credentials and configuration.
    - Events are deleted if they fall completely outside the specified free time slots.
    """
    url = os.getenv('SOGO_CALENDAR_URL')
    username = os.getenv('SOGO_USERNAME')
    password = os.getenv('SOGO_PASSWORD')

    client = DAVClient(url=url, username=username, password=password)
    calendar__ = client.calendar(url=os.getenv('SOGO_CALENDAR_URL'))

    start = datetime.now()
    end = datetime.now() + timedelta(days=int(os.getenv('DAYS_TO_UPDATE')))
    events_to_delete = calendar__.date_search(start, end)


    for free_slot in time_range:
        free_start = parse(free_slot['start'])
        free_end = parse(free_slot['end'])
        for event in events_to_delete:
            event_start = event.vobject_instance.vevent.dtstart.value
            event_end = event.vobject_instance.vevent.dtend.value
            if (free_start <= event_start < free_end) or (free_start < event_end <= free_end) or (event_start <= free_start and event_end >= free_end):
                events_to_delete.remove(event)

    for event in events_to_delete:
        event.delete()
