from datetime import datetime, timedelta


# Convert string to datetime
def parse_datetime(dt_str):
    """
    Convert a string representation of a date and time to a datetime object.

    This function uses the `fromisoformat` method to parse the input string,
    which should be in ISO format (YYYY-MM-DD[*HH[:MM[:SS[.fff[fff]]]][+HH:MM[:SS[.ffffff]]]])

    Args:
        dt_str (str): A string representing a date and time in ISO format.

    Returns:
        datetime: A datetime object representing the parsed date and time.

    Raises:
        ValueError: If the input string is not in a valid ISO format.
    """
    return datetime.fromisoformat(dt_str)

def calculate_free_times(lessons):
    """
    Calculate the free time slots from a list of scheduled lessons.

    This function takes a list of lessons, where each lesson is represented as a dictionary with 'start' and 'end' keys.
    It then calculates the free time slots by compressing the scheduled lessons and merging overlapping time slots.

    Args:
        lessons (list): A list of dictionaries, where each dictionary represents a lesson with 'start' and 'end' keys.

    Returns:
        list: A list of dictionaries representing the free time slots. Each dictionary contains 'start' and 'end' keys.

    Example:
        lessons = [
            {'start': '2022-01-01 09:00', 'end': '2022-01-01 11:00'},
            {'start': '2022-01-01 10:00', 'end': '2022-01-01 12:00'},
            {'start': '2022-01-01 13:00', 'end': '2022-01-01 14:00'}
        ]
        free_times = calculate_free_times(lessons)
        print(free_times)
        
    ## Output:
        [{'start': '2022-01-01 09:00', 'end': '2022-01-01 10:00'}, {'start': '2022-01-01 12:00', 'end': '2022-01-01 13:00'}]
    """
    cleaned_data = [{'start': entry['start'], 'end': entry['end']} for entry in lessons]
    sorted_data = sorted(cleaned_data, key=lambda x: x['start'])
    compressed_data = []
    for entry in sorted_data:
        if compressed_data and compressed_data[-1]['end'] == entry['start']:
            compressed_data[-1]['end'] = entry['end']
        else:
            compressed_data.append(entry)
            
    return compressed_data

