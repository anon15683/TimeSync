from caldav import DAVClient
import traceback
from datetime import datetime, timedelta
from icalendar import Event, Alarm
import uuid
from icalendar import Calendar
from dotenv import load_dotenv
import tqdm
import os

load_dotenv(override=True)

url = os.getenv('CALENDAR_URL')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

# Connect to the server
client = DAVClient(url=url, username=username, password=password)
principal = client.principal()

calendar__ = client.calendar(url=url)

events = calendar__.events()

for event in tqdm.tqdm(events, desc="Deleting events"):
    event.delete()
