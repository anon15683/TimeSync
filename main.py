from get_data import get_data
from get_cookies import get_cookies
from datetime import datetime, timedelta, timezone
from handle_data import handle_data
from compress_events import compress_events
from add_event import add_event
from clean_up_events import calculate_free_times
from set_free_time_in_calander import remove_events_in_time_range
import threading
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os
import time

load_dotenv(override=True)

def print_with_timestamp(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\033[97m[{timestamp}]\033[0m {message}")

def get_current_date_and_days_later():
    today = datetime.now(timezone.utc)
    days_later = today + timedelta(days=int(os.getenv('DAYS_TO_ADD')))
    return today.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), days_later.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def process_event(event):
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
    bar_length = int(os.getenv("PRINT_BAR_LENGTH", 50))
    progress = processed / total
    block = int(round(bar_length * progress))
    bar = "#" * block + "-" * (bar_length - block)
    print(f"\r\033[92mProcessing events: [{bar}] {processed}/{total} ({progress * 100:.2f}%)\033[0m")

def process_event_with_progress(event, lock, processed_events, total_events, last_print_time):
    process_event(event)
    with lock:
        processed_events[0] += 1
        current_time = time.time()
        if processed_events[0] == total_events or (current_time - last_print_time[0] >= int(os.getenv('SLEEP_PRINT_DELAY_SECONDS', 10)) / 2):
            print_progress_bar(processed_events[0], total_events)
            last_print_time[0] = current_time

def process_free_time_range(time_range, lock, processed_free_times, total_free_times, last_print_time_free):
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

    current_date, days_later = get_current_date_and_days_later()
    print_with_timestamp(f"\033[96mCurrent date: {current_date}\033[0m")
    print_with_timestamp(f"\033[96m{os.getenv('DAYS_TO_ADD')} days later: {days_later}\033[0m")

    print_with_timestamp("\033[94mGetting data...\033[0m")
    data = get_data(current_date, days_later, session_id, auth_token)
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
    print_progress_bar(total_events, total_events)  # Ensure final progress bar is printed

    print_with_timestamp("\033[92mAll events processed.\033[0m")
    print_with_timestamp("\033[92mAdded events to calendar\033[0m")
    
    print_with_timestamp("\033[94mCalculating free times...\033[0m")
    free_times = calculate_free_times(compressed_data)
    
    print_with_timestamp("\033[92mCalculated free times\033[0m")
    print_with_timestamp("\033[94mRemoving free times from calendar...\033[0m")
    
    total_free_times = len(free_times)
    processed_free_times = [0]
    last_print_time_free = [time.time()]

    with ThreadPoolExecutor() as executor:
        executor.map(lambda time_range: process_free_time_range(time_range, lock, processed_free_times, total_free_times, last_print_time_free), free_times)
    print_progress_bar(total_free_times, total_free_times)  # Ensure final progress bar is printed

    print_with_timestamp("\033[92mAll free times removed.\033[0m")

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
