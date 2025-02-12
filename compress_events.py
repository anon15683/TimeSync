def compress_events(data):
    compressed_lessons = []
    current_lesson = None

    for lesson in data["lessons"]:
        if current_lesson is None:
            current_lesson = lesson
        else:
            if (current_lesson['SubjectName'] == lesson['SubjectName'] and
                current_lesson['StudentClassName'] == lesson['StudentClassName'] and
                current_lesson['TeacherName'] == lesson['TeacherName'] and
                current_lesson['RoomName'] == lesson['RoomName'] and
                current_lesson['end'] == lesson['start']):
                current_lesson['end'] = lesson['end']
            else:
                compressed_lessons.append(current_lesson)
                current_lesson = lesson

    if current_lesson is not None:
        compressed_lessons.append(current_lesson)

    return compressed_lessons