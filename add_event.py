from caldav import DAVClient
from datetime import datetime, timedelta
from icalendar import Event, Alarm
from icalendar import Calendar
from dotenv import load_dotenv
import os
import hashlib

load_dotenv(override=True)

def add_event(subject, start_time, end_time, teacher, additional_teachers, room, additional_rooms, class_name):
    """
    Add a new event to the SOGo calendar or update an existing one.

    This function creates a new calendar event with the given details or updates an existing event
    if one with the same start and end time already exists. It also adds an alarm to the event.

    Parameters:
    subject (str): The subject or title of the event.
    start_time (datetime): The start time of the event.
    end_time (datetime): The end time of the event.
    teacher (str): The primary teacher for the event.
    additional_teachers (list): A list of additional teachers for the event.
    room (str): The primary room for the event.
    additional_rooms (list): A list of additional rooms for the event.
    class_name (str): The name of the class associated with the event.

    Returns:
    None

    Note:
    The function uses environment variables for calendar URL, username, and password.
    It creates a unique ID for each event based on its details.
    If an event with the same start and end time exists, it's replaced with the new event.
    Events in the past (end time before current time) are not added.
    """
    url = os.getenv('CALENDAR_URL')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    client = DAVClient(url=url, username=username, password=password)

    calendar__ = client.calendar(url=url)

    caldata = Calendar()

    uid_string = f"{subject}-{start_time}-{end_time}-{teacher}-{additional_teachers}-{room}-{additional_rooms}-{class_name}"
    uid = hashlib.md5(uid_string.encode('utf-8')).hexdigest()
    event = Event()
    event.add("dtstamp", datetime.now())
    event.add("dtstart", start_time)
    event.add("dtend", end_time)
    event.add("uid", uid)
    event.add("class", "PRIVATE")
    event.add("summary", subject)
    description = f"Klasse: {class_name}\nLehrer: {teacher}"
    if additional_teachers:
        description += f"\nZusätzliche Lehrer: {', '.join(additional_teachers)}"
    event.add("description", description)
    location = f"Raum: {room}"
    if additional_rooms:
        location += f"\nZusätzliche Räume: {', '.join(additional_rooms)}"
    event.add("location", location)
    caldata.add_component(event)

    alarm = Alarm()
    alarm.add("action", "DISPLAY")
    alarm.add("description", "Reminder")
    alarm.add("trigger", timedelta(minutes=-5))
    event.add_component(alarm)

    new_event = caldata.to_ical()
    start = datetime.now()
    end = datetime.now() + timedelta(days=int(os.getenv('DAYS_TO_UPDATE')))
    existing_events = calendar__.date_search(start, end)
    event_exists = False
    for existing_event in existing_events:
        if existing_event.vobject_instance.vevent.dtstart.value == start_time and existing_event.vobject_instance.vevent.dtend.value == end_time:
            if existing_event.vobject_instance.vevent.uid.value != str(uid):
                event_exists = True
                existing_event.delete()
                calendar__.save_event(new_event)

    if end_time < datetime.now().astimezone():
        return

    if not event_exists:
        calendar__.save_event(new_event)

