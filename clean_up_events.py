from datetime import datetime, timedelta


# Convert string to datetime
def parse_datetime(dt_str):
    return datetime.fromisoformat(dt_str)

# Calculate free times
def calculate_free_times(lessons):
    free_times = []
    lessons = sorted(lessons, key=lambda x: parse_datetime(x['start']))
    
    # Define the start and end of the day
    day_start = parse_datetime(lessons[0]['start']).replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)
    
    # Check for free time before the first lesson
    if parse_datetime(lessons[0]['start']) > day_start:
        free_times.append({'start': day_start.isoformat(), 'end': lessons[0]['start']})
    
    # Check for free times between lessons
    for i in range(len(lessons) - 1):
        end_current = parse_datetime(lessons[i]['end'])
        start_next = parse_datetime(lessons[i + 1]['start'])
        if end_current < start_next:
            free_times.append({'start': end_current.isoformat(), 'end': start_next.isoformat()})
    
    # Check for free time after the last lesson
    if parse_datetime(lessons[-1]['end']) < day_end:
        free_times.append({'start': lessons[-1]['end'], 'end': day_end.isoformat()})
    
    return free_times[1:]

