from datetime import datetime
from database import cursor

def check_student_exists(student_id):
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    return cursor.fetchone()

def check_schedule_exists(schedule_id):
    cursor.execute("SELECT * FROM schedules WHERE id = ?", (schedule_id,))
    return cursor.fetchone()

def convert_time(time_text):
    return datetime.strptime(time_text, "%H:%M")

def time_overlap(start1, end1, start2, end2):
    return start1 < end2 and end1 > start2
