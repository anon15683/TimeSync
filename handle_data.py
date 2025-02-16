def handle_data(data):
    """
    Process and filter lesson data, excluding lessons with 'StudioTimes' in the subject name.

    This function takes a dictionary of lesson data, filters out lessons with 'StudioTimes'
    in the subject name, and restructures the remaining lesson information into a new format.

    Args:
        data (dict): A dictionary containing a 'lessons' key with a list of lesson dictionaries.
                     Each lesson dictionary should have keys for 'SubjectName', 'start', 'end',
                     'StudentClassName', 'TeacherName', 'AdditionalTeacherNamesString',
                     'RoomName', and 'AdditionalRooms'.

    Returns:
        dict: A dictionary with a 'lessons' key containing a list of filtered and reformatted
              lesson dictionaries. Each lesson dictionary in the output contains:
              - 'start': Lesson start time (string)
              - 'end': Lesson end time (string)
              - 'SubjectName': Name of the subject (string)
              - 'StudentClassName': Name of the student class (string)
              - 'TeacherName': Name of the primary teacher (string)
              - 'AdditionalTeacherNamesString': List of additional teachers (list of strings)
              - 'RoomName': Name of the primary room (string)
              - 'AdditionalRooms': List of additional rooms (list of strings)
    """
    filtered_lessons = []

    for lesson in data["lessons"]:
        if not lesson["SubjectName"].startswith("StudioTimes"):
            filtered_lessons.append(lesson)

    filtered_lessons_json = {"lessons": []}

    for lesson in filtered_lessons:
        filtered_lessons_json["lessons"].append({
            "start": str(lesson["start"]),
            "end": str(lesson["end"]),
            "SubjectName": str(lesson["SubjectName"]),
            "StudentClassName": str(lesson["StudentClassName"]),
            "TeacherName": str(lesson["TeacherName"]),
            "AdditionalTeacherNamesString": list(lesson["AdditionalTeacherNamesString"].split(",")[1:]) if lesson["AdditionalTeacherNamesString"] else [],
            "RoomName": str(lesson["RoomName"]),
            "AdditionalRooms": list(lesson["AdditionalRooms"].split(",")[1:]) if lesson["AdditionalRooms"] else []
        })

    return filtered_lessons_json

