from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import threading
import os
import time

from get_data import get_data
from get_cookies import get_cookies
from handle_data import handle_data
from compress_events import compress_events
from add_event import add_event
from clean_up_events import calculate_free_times
from set_free_time_in_calander import remove_events_in_time_range
from get_user_id import get_user_id
from get_school_id import get_school_id

load_dotenv(override=True)

def print_with_timestamp(message):
    """
    Print a message with a timestamp prefix.

    This function takes a message and prints it to the console with a timestamp
    prefix. The timestamp is in the format "YYYY-MM-DD HH:MM:SS".

    Args:
        message (str): The message to be printed.

    Returns:
        None

    Note:
        The timestamp is printed in white color (ANSI color code 97),
        while the message retains its original color.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\033[97m[{timestamp}]\033[0m {message}")


def get_current_date_and_days_later():
    """
    Get the current date and a future date based on the 'DAYS_TO_ADD' environment variable.

    This function calculates two dates:
    1. The current date and time in UTC.
    2. A future date that is 'DAYS_TO_ADD' days from the current date.

    The 'DAYS_TO_ADD' value is read from the environment variables.

    Returns:
        tuple: A tuple containing two strings:
            - The current date and time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sssZ).
            - The future date and time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sssZ).

    Note:
        Both dates are returned as UTC timestamps.
    """
    today = datetime.now(timezone.utc)
    days_later = today + timedelta(days=int(os.getenv('DAYS_TO_ADD')))
    return today.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), days_later.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def process_event(event):
    """
    Process a single event and add it to the calendar.

    This function extracts relevant information from the event dictionary
    and calls the add_event function to add the event to the calendar.

    Args:
        event (dict): A dictionary containing event information with the following keys:
            - 'SubjectName': The name of the subject (str)
            - 'start': The start time of the event (str in format "%Y-%m-%dT%H:%M:%S%z")
            - 'end': The end time of the event (str in format "%Y-%m-%dT%H:%M:%S%z")
            - 'TeacherName': The name of the primary teacher (str)
            - 'AdditionalTeacherNamesString': Names of additional teachers (str)
            - 'RoomName': The name of the primary room (str)
            - 'AdditionalRooms': Names of additional rooms (str)
            - 'StudentClassName': The name of the student class (str)

    Returns:
        None

    Note:
        This function does not return any value but calls the add_event function
        to add the processed event to the calendar.
    """
    subject = event['SubjectName']
    start_time = datetime.strptime(event['start'], "%Y-%m-%dT%H:%M:%S%z")
    end_time = datetime.strptime(event['end'], "%Y-%m-%dT%H:%M:%S%z")
    teacher = event['TeacherName']
    additional_teachers = event['AdditionalTeacherNamesString']
    room = event['RoomName']
    additional_rooms = event['AdditionalRooms']
    class_name = event['StudentClassName']
    add_event(subject, start_time, end_time, teacher, additional_teachers, room, additional_rooms, class_name)


def print_progress_bar(processed, total):
    """
    Print a progress bar to the console showing the current progress of a task.

    This function creates and prints a visual progress bar based on the number of
    processed items and the total number of items. The progress bar is colored
    green and includes a percentage completion.

    Args:
        processed (int): The number of items that have been processed.
        total (int): The total number of items to be processed.

    Returns:
        None

    Note:
        The length of the progress bar is determined by the 'PRINT_BAR_LENGTH'
        environment variable, defaulting to 50 if not set.
    """
    bar_length = int(os.getenv("PRINT_BAR_LENGTH", 50))
    progress = processed / total
    block = int(round(bar_length * progress))
    bar = "#" * block + "-" * (bar_length - block)
    print(f"\r\033[92mProcessing events: [{bar}] {processed}/{total} ({progress * 100:.2f}%)\033[0m")


def process_event_with_progress(event, lock, processed_events, total_events, last_print_time):
    """
    Processes an event and updates the progress bar.

    Args:
        event: The event to be processed.
        lock: A threading lock to ensure thread-safe updates to the processed_events counter.
        processed_events (list): A list containing a single integer representing the number of processed events.
        total_events (int): The total number of events to be processed.
        last_print_time (list): A list containing a single float representing the last time the progress bar was printed.

    Returns:
        None
    """
    process_event(event)
    with lock:
        processed_events[0] += 1
        current_time = time.time()
        if processed_events[0] == total_events or (current_time - last_print_time[0] >= int(os.getenv('SLEEP_PRINT_DELAY_SECONDS', 10)) / 2):
            print_progress_bar(processed_events[0], total_events)
            last_print_time[0] = current_time


def process_free_time_range(time_range, lock, processed_free_times, total_free_times, last_print_time_free):
    """
    Processes a given time range by removing events within that range and updating the progress.

    Args:
        time_range (tuple): The time range to process.
        lock (threading.Lock): A lock to ensure thread-safe operations.
        processed_free_times (list): A list containing the count of processed free times.
        total_free_times (int): The total number of free times to process.
        last_print_time_free (list): A list containing the last time the progress was printed.

    Returns:
        None
    """
    remove_events_in_time_range(time_range)
    with lock:
        processed_free_times[0] += 1
        current_time = time.time()
        if processed_free_times[0] == total_free_times or (current_time - last_print_time_free[0] >= int(os.getenv('SLEEP_PRINT_DELAY_SECONDS', 10)) / 2):
            print_progress_bar(processed_free_times[0], total_free_times)
            last_print_time_free[0] = current_time

def main():
    print_with_timestamp("\033[94mLogging in...\033[0m")
    session_id, auth_token = get_cookies()
    print_with_timestamp("\033[92mLogged in\033[0m")

    print_with_timestamp("\033[94mGetting user ID...\033[0m")
    user_id = get_user_id(session_id, auth_token)
    print_with_timestamp("\033[94mGot user ID\033[0m")
    
    print_with_timestamp("\033[94mGetting school ID...\033[0m")
    school_id = get_school_id(session_id, auth_token)
    print_with_timestamp("\033[94mGot school ID\033[0m")

    print_with_timestamp("\033[94mGetting current date and days later...\033[0m")
    current_date, days_later = get_current_date_and_days_later()
    print_with_timestamp(f"\033[96mCurrent date: {current_date}\033[0m")
    print_with_timestamp(f"\033[96m{os.getenv('DAYS_TO_ADD')} days later: {days_later}\033[0m")

    print_with_timestamp("\033[94mGetting data...\033[0m")
    data = get_data(current_date, days_later, session_id, auth_token, user_id, school_id)
    print_with_timestamp("\033[92mGot data\033[0m")

    print_with_timestamp("\033[94mHandling data...\033[0m")
    parsed_data = handle_data(data)
    print_with_timestamp("\033[92mHandled data\033[0m")

    print_with_timestamp("\033[94mCompressing events...\033[0m")
    compressed_data = compress_events(parsed_data)
    print_with_timestamp("\033[92mCompressed events\033[0m")

    print_with_timestamp("\033[94mAdding events to calendar...\033[0m")
    total_events = len(compressed_data)
    processed_events = [0]
    lock = threading.Lock()
    last_print_time = [time.time()]

    with ThreadPoolExecutor() as executor:
        executor.map(lambda event: process_event_with_progress(event, lock, processed_events, total_events, last_print_time), compressed_data)
    print_progress_bar(total_events, total_events)
    print_with_timestamp("\033[92mAll events processed.\033[0m")
    print_with_timestamp("\033[92mAdded events to calendar\033[0m")
    
    print_with_timestamp("\033[94mCalculating free times...\033[0m")
    free_times = calculate_free_times(compressed_data)
    print_with_timestamp("\033[92mCalculated free times\033[0m")
    
    print_with_timestamp("\033[94mRemoving events from calendar...\033[0m")
    remove_events_in_time_range(free_times)
    print_with_timestamp("\033[92mRemoved events from calendar\033[0m")

if __name__ == "__main__":
    interval_minutes = int(os.getenv('INTERVAL_MINUTES', 10))
    while True:
        start_time = time.time()
        main()
        end_time = time.time()
        iteration_duration = end_time - start_time
        print_with_timestamp(f"\033[94mIteration took {iteration_duration:.2f} seconds.\033[0m")
        sleep_time = interval_minutes * 60
        interval = int(os.getenv('SLEEP_PRINT_DELAY_SECONDS', 10))
        bar_length = int(os.getenv("PRINT_BAR_LENGTH", 50))
        for i in range(0, sleep_time, interval):
            progress = i / sleep_time
            block = int(round(bar_length * progress))
            bar = "#" * block + "-" * (bar_length - block)
            print(f"\r\033[93mSleeping: [{bar}] {i // interval}/{sleep_time // interval} ({progress * 100:.2f}%) - {sleep_time - i} seconds remaining\033[0m")
            time.sleep(interval)
        print_with_timestamp(f"\r\033[93mSleeping: [{'#' * bar_length}] {sleep_time // interval}/{sleep_time // interval} (100.00%) - 0 seconds remaining\033[0m")
