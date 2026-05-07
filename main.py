import tkinter as tk
from database import conn, cursor
from config import BG_COLOR, SIDEBAR_COLOR, FRAME_COLOR, TEXT_COLOR, SUBTEXT_COLOR, FONT_TITLE, FONT_HEADER, FONT_MAIN
from ui_helpers import show_page, make_page_title, make_panel, make_label, make_entry, make_button, make_listbox, make_sidebar_button
from students import add_student, view_students, delete_student, edit_student
from schedules import add_schedule, view_schedules, delete_schedule, edit_schedule
from attendance import mark_attendance, view_attendance_records, delete_attendance, calculate_attendance

root = tk.Tk()
root.title("Attendance and Scheduling System")
root.geometry("1100x720")
root.configure(bg=BG_COLOR)

main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True)

sidebar_frame = tk.Frame(main_frame, bg=SIDEBAR_COLOR, width=230)
sidebar_frame.pack(side="left", fill="y")
sidebar_frame.pack_propagate(False)

content_frame = tk.Frame(main_frame, bg=BG_COLOR)
content_frame.pack(side="right", fill="both", expand=True)

dashboard_page = tk.Frame(content_frame, bg=BG_COLOR)
student_page = tk.Frame(content_frame, bg=BG_COLOR)
schedule_page = tk.Frame(content_frame, bg=BG_COLOR)
attendance_page = tk.Frame(content_frame, bg=BG_COLOR)

pages = [dashboard_page, student_page, schedule_page, attendance_page]

make_page_title(
    dashboard_page,
    "Dashboard",
    "Welcome. Use the menu on the left to manage students, schedules, and attendance records."
)

dashboard_panel = make_panel(dashboard_page, "System Overview")

tk.Label(
    dashboard_panel,
    text=(
        "This system helps students manage attendance and academic schedules.\n\n"
        "• Records attendance per student and class schedule\n"
        "• Prevents duplicate attendance records per class per day\n"
        "• Detects overlapping schedule entries\n"
        "• Adjusts schedules based on priority\n"
        "• Stores records using SQLite database storage"
    ),
    bg=FRAME_COLOR,
    fg=TEXT_COLOR,
    font=FONT_MAIN,
    justify="left"
).pack(anchor="w", pady=5)

tk.Label(
    dashboard_panel,
    text="Current Records",
    bg=FRAME_COLOR,
    fg=TEXT_COLOR,
    font=FONT_HEADER
).pack(anchor="w", pady=(20, 5))

student_count_label = tk.Label(dashboard_panel, text="Students: 0", bg=FRAME_COLOR, fg=TEXT_COLOR, font=FONT_MAIN)
student_count_label.pack(anchor="w")

schedule_count_label = tk.Label(dashboard_panel, text="Schedules: 0", bg=FRAME_COLOR, fg=TEXT_COLOR, font=FONT_MAIN)
schedule_count_label.pack(anchor="w")

attendance_count_label = tk.Label(dashboard_panel, text="Attendance Records: 0", bg=FRAME_COLOR, fg=TEXT_COLOR, font=FONT_MAIN)
attendance_count_label.pack(anchor="w")

def update_dashboard():
    cursor.execute("SELECT COUNT(*) FROM students")
    student_count_label.config(text=f"Students: {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM schedules")
    schedule_count_label.config(text=f"Schedules: {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM attendance")
    attendance_count_label.config(text=f"Attendance Records: {cursor.fetchone()[0]}")

def close_app():
    conn.close()
    root.destroy()

make_page_title(student_page, "Student Management", "Add, edit, and delete student records.")

student_panel = make_panel(student_page, "Student Records")

make_label(student_panel, "Student Name:", 0, 0)
student_entry = make_entry(student_panel, 0, 1, width=30)
make_button(student_panel, "Add Student", lambda: add_student(student_entry, student_list, update_dashboard), 0, 2)

student_list = make_listbox(student_panel, 1, 0, height=8, columnspan=4)

make_label(student_panel, "Student ID to Delete:", 2, 0)
student_delete_entry = make_entry(student_panel, 2, 1, width=15)
make_button(student_panel, "Delete Student", lambda: delete_student(student_delete_entry, student_list, attendance_list, update_dashboard, view_attendance_records), 2, 2, danger=True)

make_label(student_panel, "Student ID to Edit:", 3, 0)
student_edit_id_entry = make_entry(student_panel, 3, 1, width=15)

make_label(student_panel, "New Name:", 4, 0)
student_edit_name_entry = make_entry(student_panel, 4, 1, width=30)
make_button(student_panel, "Edit Student", lambda: edit_student(student_edit_id_entry, student_edit_name_entry, student_list, attendance_list, view_attendance_records), 4, 2)

make_page_title(schedule_page, "Schedule Management", "Add schedules, detect conflicts, and adjust time slots based on priority.")

schedule_panel = make_panel(schedule_page, "Schedule Records")

make_label(schedule_panel, "Class/Task Name:", 0, 0)
task_entry = make_entry(schedule_panel, 0, 1, width=30)

make_label(schedule_panel, "Start Time HH:MM:", 1, 0)
start_entry = make_entry(schedule_panel, 1, 1, width=30)

make_label(schedule_panel, "End Time HH:MM:", 2, 0)
end_entry = make_entry(schedule_panel, 2, 1, width=30)

make_label(schedule_panel, "Priority:", 3, 0)
priority_entry = make_entry(schedule_panel, 3, 1, width=30)

make_label(schedule_panel, "Priority guide: 1 = highest priority, 2 = medium, 3 = lower", 4, 0, columnspan=3)
make_button(schedule_panel, "Add Schedule", lambda: add_schedule(task_entry, start_entry, end_entry, priority_entry, schedule_list, update_dashboard), 5, 1)

schedule_list = make_listbox(schedule_panel, 6, 0, height=7, columnspan=4)

make_label(schedule_panel, "Schedule ID to Delete:", 7, 0)
schedule_id_entry = make_entry(schedule_panel, 7, 1, width=15)
make_button(schedule_panel, "Delete Schedule", lambda: delete_schedule(schedule_id_entry, schedule_list, attendance_list, update_dashboard, view_attendance_records), 7, 2, danger=True)

make_label(schedule_panel, "Schedule ID to Edit:", 8, 0)
schedule_edit_id_entry = make_entry(schedule_panel, 8, 1, width=15)

make_label(schedule_panel, "New Class/Task:", 9, 0)
schedule_edit_task_entry = make_entry(schedule_panel, 9, 1, width=30)

make_label(schedule_panel, "New Start HH:MM:", 10, 0)
schedule_edit_start_entry = make_entry(schedule_panel, 10, 1, width=30)

make_label(schedule_panel, "New End HH:MM:", 11, 0)
schedule_edit_end_entry = make_entry(schedule_panel, 11, 1, width=30)

make_label(schedule_panel, "New Priority:", 12, 0)
schedule_edit_priority_entry = make_entry(schedule_panel, 12, 1, width=30)
make_button(schedule_panel, "Edit Schedule", lambda: edit_schedule(schedule_edit_id_entry, schedule_edit_task_entry, schedule_edit_start_entry, schedule_edit_end_entry, schedule_edit_priority_entry, schedule_list, attendance_list, view_attendance_records), 12, 2)

make_page_title(attendance_page, "Attendance", "Mark attendance per student and schedule/class.")

attendance_panel = make_panel(attendance_page, "Attendance Records")

make_label(attendance_panel, "Student ID:", 0, 0)
student_id_entry = make_entry(attendance_panel, 0, 1, width=15)

make_label(attendance_panel, "Schedule ID:", 0, 2)
schedule_attendance_entry = make_entry(attendance_panel, 0, 3, width=15)

make_button(attendance_panel, "Mark Present", lambda: mark_attendance("Present", student_id_entry, schedule_attendance_entry, attendance_list, update_dashboard), 1, 0)
make_button(attendance_panel, "Mark Absent", lambda: mark_attendance("Absent", student_id_entry, schedule_attendance_entry, attendance_list, update_dashboard), 1, 1)
make_button(attendance_panel, "Calculate %", lambda: calculate_attendance(student_id_entry), 1, 2)

attendance_list = make_listbox(attendance_panel, 2, 0, height=9, columnspan=5)

make_label(attendance_panel, "Attendance ID to Delete:", 3, 0)
attendance_id_entry = make_entry(attendance_panel, 3, 1, width=15)
make_button(attendance_panel, "Delete Attendance", lambda: delete_attendance(attendance_id_entry, attendance_list, update_dashboard), 3, 2, danger=True)

tk.Label(
    sidebar_frame,
    text="ATTENDANCE\nSYSTEM",
    bg=SIDEBAR_COLOR,
    fg=TEXT_COLOR,
    font=FONT_TITLE,
    justify="left"
).pack(anchor="w", padx=25, pady=(35, 10))

tk.Label(
    sidebar_frame,
    text="Main Menu",
    bg=SIDEBAR_COLOR,
    fg=TEXT_COLOR,
    font=FONT_HEADER
).pack(anchor="w", padx=25, pady=(0, 20))

def refresh_all():
    view_students(student_list)
    view_schedules(schedule_list)
    view_attendance_records(attendance_list)
    update_dashboard()

make_sidebar_button(sidebar_frame, "Dashboard", lambda: show_page(dashboard_page, pages, refresh_all))
make_sidebar_button(sidebar_frame, "Students", lambda: show_page(student_page, pages, refresh_all))
make_sidebar_button(sidebar_frame, "Schedules", lambda: show_page(schedule_page, pages, refresh_all))
make_sidebar_button(sidebar_frame, "Attendance", lambda: show_page(attendance_page, pages, refresh_all))
make_sidebar_button(sidebar_frame, "Exit", close_app, danger=True)

root.protocol("WM_DELETE_WINDOW", close_app)

view_students(student_list)
view_schedules(schedule_list)
view_attendance_records(attendance_list)
update_dashboard()
show_page(dashboard_page, pages, refresh_all)

root.mainloop()
