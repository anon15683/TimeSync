from caldav import DAVClient
from datetime import datetime, timedelta
from icalendar import Event, Alarm
from icalendar import Calendar
from dotenv import load_dotenv
import os
import hashlib

load_dotenv(override=True)

def add_event(subject, start_time, end_time, teacher, additional_teachers, room, additional_rooms, class_name):
    url = os.getenv('SOGO_CALENDAR_URL')
    username = os.getenv('SOGO_USERNAME')
    password = os.getenv('SOGO_PASSWORD')
    
    client = DAVClient(url=url, username=username, password=password)
    
    calendar__ = client.calendar(url=os.getenv('SOGO_CALENDAR_URL'))
    
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
