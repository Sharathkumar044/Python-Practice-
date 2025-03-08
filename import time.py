import time
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def set_reminder():
    task = task_entry.get()
    time_str = time_entry.get()
    
    try:
        reminder_time = datetime.strptime(time_str, "%H:%M").time()
        reminders.append((task, reminder_time))
        reminder_listbox.insert(tk.END, f"{time_str} - {task}")
        task_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter time in HH:MM format.")

def check_reminders():
    now = datetime.now().time()
    for task, reminder_time in reminders[:]:
        if now.hour == reminder_time.hour and now.minute == reminder_time.minute:
            messagebox.showinfo("Reminder", f"⏰ {task}")
            reminders.remove((task, reminder_time))
            reminder_listbox.delete(0, tk.END)
            for t, rt in reminders:
                reminder_listbox.insert(tk.END, f"{rt.strftime('%H:%M')} - {t}")
    root.after(60000, check_reminders)

reminders = []

# GUI Setup
root = tk.Tk()
root.title("Simple Reminder Application")
root.geometry("400x350")

tk.Label(root, text="Task to Do:").pack()
task_entry = tk.Entry(root, width=40)
task_entry.pack()

tk.Label(root, text="Time (HH:MM) 24 Hr formot:").pack()
time_entry = tk.Entry(root, width=10)
time_entry.pack()

tk.Button(root, text="Set Reminder", command=set_reminder).pack()

reminder_listbox = tk.Listbox(root, width=50)
reminder_listbox.pack()

check_reminders()
root.mainloop()