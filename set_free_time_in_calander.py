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
    url = os.getenv('CALENDAR_URL')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    client = DAVClient(url=url, username=username, password=password)
    calendar__ = client.calendar(url=url)

    start = datetime.now()
    end = datetime.now() + timedelta(days=int(os.getenv('DAYS_TO_UPDATE')))
    events_to_delete = calendar__.date_search(start, end)

    events_to_preserve = []

    free_slots = [(parse(slot['start']), parse(slot['end'])) for slot in time_range]

    for event in events_to_delete:
        event_start = event.vobject_instance.vevent.dtstart.value
        event_end = event.vobject_instance.vevent.dtend.value

        for free_start, free_end in free_slots:
            if (free_start <= event_start < free_end) or (free_start < event_end <= free_end) or (event_start >= free_start and event_end <= free_end):
                events_to_preserve.append(event)
                break

    events_to_remove = [event for event in events_to_delete if event not in events_to_preserve]

    for event in events_to_remove:
        event.delete()
