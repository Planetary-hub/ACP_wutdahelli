import tkinter as tk
from tkinter import messagebox
from database import conn, cursor
from helpers import check_student_exists

def add_student(student_entry, student_list, update_dashboard_cb):
    name = student_entry.get().strip()

    if name == "":
        messagebox.showwarning("Input Error", "Please enter a student name.")
        return

    if len(name) > 40:
        messagebox.showwarning("Input Error", "Student name must be 40 characters or less.")
        return

    cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
    conn.commit()

    student_entry.delete(0, tk.END)

    view_students(student_list)
    update_dashboard_cb()

    messagebox.showinfo("Success", "Student added successfully.")

def view_students(student_list):
    student_list.delete(0, tk.END)

    cursor.execute("SELECT * FROM students ORDER BY id")
    students = cursor.fetchall()

    if not students:
        student_list.insert(tk.END, "No students found.")
        return

    for student in students:
        student_list.insert(tk.END, f"ID: {student[0]} | Name: {student[1]}")

def delete_student(student_delete_entry, student_list, attendance_list, update_dashboard_cb, view_attendance_cb):
    student_id = student_delete_entry.get().strip()

    if student_id == "":
        messagebox.showwarning("Input Error", "Please enter a Student ID.")
        return

    if not student_id.isdigit():
        messagebox.showwarning("Input Error", "Student ID must be a number.")
        return

    student_id = int(student_id)
    student = check_student_exists(student_id)

    if not student:
        messagebox.showwarning("Error", "Student ID does not exist.")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete '{student[1]}'?\n"
        "This will also delete their attendance records."
    )

    if not confirm:
        return

    cursor.execute("DELETE FROM attendance WHERE student_id = ?", (student_id,))
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()

    student_delete_entry.delete(0, tk.END)

    view_students(student_list)
    view_attendance_cb(attendance_list)
    update_dashboard_cb()

    messagebox.showinfo("Success", "Student deleted successfully.")

def edit_student(student_edit_id_entry, student_edit_name_entry, student_list, attendance_list, view_attendance_cb):
    student_id = student_edit_id_entry.get().strip()
    new_name = student_edit_name_entry.get().strip()

    if student_id == "" or new_name == "":
        messagebox.showwarning("Input Error", "Please enter Student ID and new name.")
        return

    if not student_id.isdigit():
        messagebox.showwarning("Input Error", "Student ID must be a number.")
        return

    if len(new_name) > 40:
        messagebox.showwarning("Input Error", "Student name must be 40 characters or less.")
        return

    student_id = int(student_id)
    student = check_student_exists(student_id)

    if not student:
        messagebox.showwarning("Error", "Student ID does not exist.")
        return

    cursor.execute(
        "UPDATE students SET name = ? WHERE id = ?",
        (new_name, student_id)
    )
    conn.commit()

    student_edit_id_entry.delete(0, tk.END)
    student_edit_name_entry.delete(0, tk.END)

    view_students(student_list)
    view_attendance_cb(attendance_list)

    messagebox.showinfo("Success", "Student name updated successfully.")
