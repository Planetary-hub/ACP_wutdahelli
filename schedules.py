import tkinter as tk
from tkinter import messagebox
from datetime import timedelta
from database import conn, cursor
from helpers import check_schedule_exists, convert_time, time_overlap

def find_available_slot(start_time, end_time, priority):
    duration = end_time - start_time
    break_time = timedelta(minutes=0)
    messages = []

    while True:
        cursor.execute("SELECT * FROM schedules ORDER BY start_time")
        schedules = cursor.fetchall()

        conflict_found = False

        for sched in schedules:
            schedule_id = sched[0]
            old_task = sched[1]
            old_start = convert_time(sched[2])
            old_end = convert_time(sched[3])
            old_priority = sched[4]

            if time_overlap(start_time, end_time, old_start, old_end):
                conflict_found = True

                if priority < old_priority:
                    old_duration = old_end - old_start

                    adjusted_start = end_time + break_time
                    adjusted_end = adjusted_start + old_duration

                    adjusted_start, adjusted_end, adjustment_message = find_available_slot(
                        adjusted_start,
                        adjusted_end,
                        old_priority
                    )

                    cursor.execute(
                        "UPDATE schedules SET start_time = ?, end_time = ? WHERE id = ?",
                        (
                            adjusted_start.strftime("%H:%M"),
                            adjusted_end.strftime("%H:%M"),
                            schedule_id
                        )
                    )

                    conn.commit()

                    messages.append(
                        f"Conflict with '{old_task}'. "
                        f"Existing lower-priority task was moved to "
                        f"{adjusted_start.strftime('%H:%M')} - {adjusted_end.strftime('%H:%M')}."
                    )

                    if adjustment_message != "No conflict detected.":
                        messages.append(adjustment_message)

                    break

                else:
                    start_time = old_end + break_time
                    end_time = start_time + duration

                    messages.append(
                        f"Conflict with '{old_task}'. "
                        f"New task was moved to "
                        f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}."
                    )

                    break

        if not conflict_found:
            if messages:
                return start_time, end_time, "\n".join(messages)
            else:
                return start_time, end_time, "No conflict detected."

def add_schedule(task_entry, start_entry, end_entry, priority_entry, schedule_list, update_dashboard_cb):
    task = task_entry.get().strip()
    start = start_entry.get().strip()
    end = end_entry.get().strip()
    priority_text = priority_entry.get().strip()

    if task == "" or start == "" or end == "" or priority_text == "":
        messagebox.showwarning("Input Error", "Please complete all schedule fields.")
        return

    if len(task) > 40:
        messagebox.showwarning("Input Error", "Class/Task name must be 40 characters or less.")
        return

    if not priority_text.isdigit():
        messagebox.showwarning("Input Error", "Priority must be a number.")
        return

    priority = int(priority_text)

    if priority <= 0:
        messagebox.showwarning("Input Error", "Priority must be 1 or higher.")
        return

    try:
        new_start = convert_time(start)
        new_end = convert_time(end)
    except ValueError:
        messagebox.showwarning("Input Error", "Use HH:MM format for time. Example: 08:30")
        return

    if new_start >= new_end:
        messagebox.showwarning("Input Error", "Start time must be earlier than end time.")
        return

    final_start, final_end, conflict_message = find_available_slot(new_start, new_end, priority)

    cursor.execute(
        "INSERT INTO schedules (task_name, start_time, end_time, priority) VALUES (?, ?, ?, ?)",
        (
            task,
            final_start.strftime("%H:%M"),
            final_end.strftime("%H:%M"),
            priority
        )
    )

    conn.commit()

    task_entry.delete(0, tk.END)
    start_entry.delete(0, tk.END)
    end_entry.delete(0, tk.END)
    priority_entry.delete(0, tk.END)

    view_schedules(schedule_list)
    update_dashboard_cb()

    messagebox.showinfo(
        "Schedule Added",
        f"{conflict_message}\n\n"
        f"Final schedule for '{task}': "
        f"{final_start.strftime('%H:%M')} - {final_end.strftime('%H:%M')}"
    )

def view_schedules(schedule_list):
    schedule_list.delete(0, tk.END)

    cursor.execute("SELECT * FROM schedules ORDER BY start_time")
    schedules = cursor.fetchall()

    if not schedules:
        schedule_list.insert(tk.END, "No schedules found.")
        return

    for sched in schedules:
        schedule_list.insert(
            tk.END,
            f"ID: {sched[0]} | {sched[1]} | {sched[2]} - {sched[3]} | Priority: {sched[4]}"
        )

def delete_schedule(schedule_id_entry, schedule_list, attendance_list, update_dashboard_cb, view_attendance_cb):
    schedule_id = schedule_id_entry.get().strip()

    if schedule_id == "":
        messagebox.showwarning("Input Error", "Please enter Schedule ID.")
        return

    if not schedule_id.isdigit():
        messagebox.showwarning("Input Error", "Schedule ID must be a number.")
        return

    schedule_id = int(schedule_id)
    schedule = check_schedule_exists(schedule_id)

    if not schedule:
        messagebox.showwarning("Error", "Schedule ID does not exist.")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete '{schedule[1]}'?\n"
        "This will also delete attendance records connected to this schedule."
    )

    if not confirm:
        return

    cursor.execute("DELETE FROM attendance WHERE schedule_id = ?", (schedule_id,))
    cursor.execute("DELETE FROM schedules WHERE id = ?", (schedule_id,))
    conn.commit()

    schedule_id_entry.delete(0, tk.END)

    view_schedules(schedule_list)
    view_attendance_cb(attendance_list)
    update_dashboard_cb()

    messagebox.showinfo("Success", "Schedule deleted successfully.")

def edit_schedule(
    schedule_edit_id_entry, schedule_edit_task_entry,
    schedule_edit_start_entry, schedule_edit_end_entry,
    schedule_edit_priority_entry, schedule_list, attendance_list, view_attendance_cb
):
    schedule_id = schedule_edit_id_entry.get().strip()
    new_task = schedule_edit_task_entry.get().strip()
    new_start = schedule_edit_start_entry.get().strip()
    new_end = schedule_edit_end_entry.get().strip()
    new_priority = schedule_edit_priority_entry.get().strip()

    if schedule_id == "":
        messagebox.showwarning("Input Error", "Please enter Schedule ID.")
        return

    if not schedule_id.isdigit():
        messagebox.showwarning("Input Error", "Schedule ID must be a number.")
        return

    schedule_id = int(schedule_id)
    schedule = check_schedule_exists(schedule_id)

    if not schedule:
        messagebox.showwarning("Error", "Schedule ID does not exist.")
        return

    task = new_task if new_task != "" else schedule[1]
    start = new_start if new_start != "" else schedule[2]
    end = new_end if new_end != "" else schedule[3]
    priority_text = new_priority if new_priority != "" else str(schedule[4])

    if len(task) > 40:
        messagebox.showwarning("Input Error", "Class/Task name must be 40 characters or less.")
        return

    if not priority_text.isdigit():
        messagebox.showwarning("Input Error", "Priority must be a number.")
        return

    priority = int(priority_text)

    if priority <= 0:
        messagebox.showwarning("Input Error", "Priority must be 1 or higher.")
        return

    try:
        start_time = convert_time(start)
        end_time = convert_time(end)
    except ValueError:
        messagebox.showwarning("Input Error", "Use HH:MM format for time. Example: 08:30")
        return

    if start_time >= end_time:
        messagebox.showwarning("Input Error", "Start time must be earlier than end time.")
        return

    cursor.execute("DELETE FROM schedules WHERE id = ?", (schedule_id,))
    conn.commit()

    final_start, final_end, conflict_message = find_available_slot(start_time, end_time, priority)

    cursor.execute(
        "INSERT INTO schedules (id, task_name, start_time, end_time, priority) VALUES (?, ?, ?, ?, ?)",
        (
            schedule_id,
            task,
            final_start.strftime("%H:%M"),
            final_end.strftime("%H:%M"),
            priority
        )
    )

    conn.commit()

    schedule_edit_id_entry.delete(0, tk.END)
    schedule_edit_task_entry.delete(0, tk.END)
    schedule_edit_start_entry.delete(0, tk.END)
    schedule_edit_end_entry.delete(0, tk.END)
    schedule_edit_priority_entry.delete(0, tk.END)

    view_schedules(schedule_list)
    view_attendance_cb(attendance_list)

    messagebox.showinfo(
        "Schedule Updated",
        f"{conflict_message}\n\n"
        f"Final schedule for '{task}': "
        f"{final_start.strftime('%H:%M')} - {final_end.strftime('%H:%M')}"
    )
