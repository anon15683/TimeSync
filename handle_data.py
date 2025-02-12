import json

def handle_data(data):
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
