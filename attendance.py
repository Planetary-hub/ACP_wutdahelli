import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from database import conn, cursor
from helpers import check_student_exists, check_schedule_exists

def mark_attendance(status, student_id_entry, schedule_attendance_entry, attendance_list, update_dashboard_cb):
    student_id = student_id_entry.get().strip()
    schedule_id = schedule_attendance_entry.get().strip()

    if student_id == "" or schedule_id == "":
        messagebox.showwarning("Input Error", "Please enter both Student ID and Schedule ID.")
        return

    if not student_id.isdigit() or not schedule_id.isdigit():
        messagebox.showwarning("Input Error", "Student ID and Schedule ID must be numbers.")
        return

    student_id = int(student_id)
    schedule_id = int(schedule_id)

    student = check_student_exists(student_id)
    if not student:
        messagebox.showwarning("Error", "Student ID does not exist.")
        return

    schedule = check_schedule_exists(schedule_id)
    if not schedule:
        messagebox.showwarning("Error", "Schedule ID does not exist.")
        return

    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    cursor.execute(
        "SELECT * FROM attendance WHERE student_id = ? AND schedule_id = ? AND date = ?",
        (student_id, schedule_id, current_date)
    )

    existing_record = cursor.fetchone()

    if existing_record:
        messagebox.showwarning(
            "Duplicate Attendance",
            "Attendance has already been recorded for this student in this class/schedule today."
        )
        return

    cursor.execute(
        "INSERT INTO attendance (student_id, schedule_id, date, time, status) VALUES (?, ?, ?, ?, ?)",
        (student_id, schedule_id, current_date, current_time, status)
    )

    conn.commit()

    student_id_entry.delete(0, tk.END)
    schedule_attendance_entry.delete(0, tk.END)

    view_attendance_records(attendance_list)
    update_dashboard_cb()

    messagebox.showinfo(
        "Success",
        f"Attendance marked as {status} for {student[1]} in {schedule[1]}."
    )

def view_attendance_records(attendance_list):
    attendance_list.delete(0, tk.END)

    cursor.execute("""
    SELECT attendance.id, students.name, schedules.task_name, schedules.start_time, schedules.end_time,
           attendance.date, attendance.time, attendance.status
    FROM attendance
    INNER JOIN students ON students.id = attendance.student_id
    INNER JOIN schedules ON schedules.id = attendance.schedule_id
    ORDER BY attendance.date DESC, attendance.time DESC
    """)

    records = cursor.fetchall()

    if not records:
        attendance_list.insert(tk.END, "No attendance records found.")
        return

    for record in records:
        attendance_id, name, task, start, end, date, time, status = record
        attendance_list.insert(
            tk.END,
            f"ID: {attendance_id} | {name} | {task} ({start}-{end}) | {date} | {time} | {status}"
        )

def delete_attendance(attendance_id_entry, attendance_list, update_dashboard_cb):
    attendance_id = attendance_id_entry.get().strip()

    if attendance_id == "":
        messagebox.showwarning("Input Error", "Please enter attendance ID.")
        return

    if not attendance_id.isdigit():
        messagebox.showwarning("Input Error", "Attendance ID must be a number.")
        return

    attendance_id = int(attendance_id)

    cursor.execute("SELECT * FROM attendance WHERE id = ?", (attendance_id,))
    record = cursor.fetchone()

    if not record:
        messagebox.showwarning("Error", "Attendance ID does not exist.")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this attendance record?"
    )

    if not confirm:
        return

    cursor.execute("DELETE FROM attendance WHERE id = ?", (attendance_id,))
    conn.commit()

    attendance_id_entry.delete(0, tk.END)

    view_attendance_records(attendance_list)
    update_dashboard_cb()

    messagebox.showinfo("Success", "Attendance record deleted successfully.")

def calculate_attendance(student_id_entry):
    student_id = student_id_entry.get().strip()

    if student_id == "":
        messagebox.showwarning("Input Error", "Please enter a student ID.")
        return

    if not student_id.isdigit():
        messagebox.showwarning("Input Error", "Student ID must be a number.")
        return

    student_id = int(student_id)
    student = check_student_exists(student_id)

    if not student:
        messagebox.showwarning("Error", "Student ID does not exist.")
        return

    cursor.execute(
        "SELECT COUNT(*) FROM attendance WHERE student_id = ?",
        (student_id,)
    )
    total_records = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM attendance WHERE student_id = ? AND status = 'Present'",
        (student_id,)
    )
    present_records = cursor.fetchone()[0]

    percentage = (present_records / total_records) * 100 if total_records > 0 else 0

    messagebox.showinfo(
        "Attendance Percentage",
        f"Student: {student[1]}\n"
        f"Present Records: {present_records}\n"
        f"Total Records: {total_records}\n"
        f"Attendance Percentage: {percentage:.2f}%"
    )
