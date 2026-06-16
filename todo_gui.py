import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import json
import os
from datetime import datetime

# ---------------- FILE ---------------- #
FILE_NAME = "tasks.json"

# ---------------- LOAD TASKS ---------------- #
def load_tasks():

    if os.path.exists(FILE_NAME):

        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)

        except:
            return []

    return []

# ---------------- SAVE TASKS ---------------- #
def save_tasks():

    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

# ---------------- TASK LIST ---------------- #
tasks = load_tasks()

# ---------------- UPDATE COUNTER ---------------- #
def update_counter():

    total = len(tasks)

    completed = len([
        task for task in tasks
        if task.get("done")
    ])

    pending = total - completed

    counter_label.config(
        text=
        f"Total Tasks: {total}    "
        f"Completed: {completed}    "
        f"Pending: {pending}"
    )

# ---------------- UPDATE LISTBOX ---------------- #
def update_listbox(filtered_tasks=None):

    task_listbox.delete(0, tk.END)

    display_tasks = filtered_tasks if filtered_tasks else tasks

    for index, task in enumerate(display_tasks):

        title = task.get("title", "No Title")

        due = task.get("due", "No Due Date")

        priority = task.get("priority", "Medium")

        done = task.get("done", False)

        if done:
            status = "✔ Completed"
            icon = "☑"

        else:
            status = "❌ Pending"
            icon = "📝"

        task_text = (
            f"{icon}  {index+1}. {title}"
            f"   |   📅 {due}"
            f"   |   ⚡ {priority}"
            f"   |   {status}"
        )

        task_listbox.insert(tk.END, task_text)

        # Priority Colors
        if priority == "High":
            task_listbox.itemconfig(index, fg="red")

        elif priority == "Medium":
            task_listbox.itemconfig(index, fg="orange")

        elif priority == "Low":
            task_listbox.itemconfig(index, fg="green")

        # Completed Task Style
        if done:
            task_listbox.itemconfig(index, fg="gray")

# ---------------- ADD TASK ---------------- #
def add_task():

    title = task_entry.get().strip()

    due = due_entry.get().strip()

    priority = priority_var.get()

    if title == "":
        messagebox.showwarning(
            "Warning",
            "Task cannot be empty!"
        )
        return

    if due == "":
        messagebox.showwarning(
            "Warning",
            "Please select due date!"
        )
        return

    task = {
        "title": title,
        "due": due,
        "priority": priority,
        "done": False
    }

    tasks.append(task)

    save_tasks()

    update_listbox()

    task_listbox.yview(tk.END)

    update_counter()

    # Clear fields
    task_entry.delete(0, tk.END)

    due_entry.delete(0, tk.END)

    priority_var.set("Medium")

# ---------------- COMPLETE TASK ---------------- #
def complete_task():

    selected = task_listbox.curselection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Select a task first!"
        )

        return

    index = selected[0]

    tasks[index]["done"] = True

    save_tasks()

    update_listbox()

    update_counter()

# ---------------- DELETE TASK ---------------- #
def delete_task():

    selected = task_listbox.curselection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Select a task first!"
        )

        return

    index = selected[0]

    confirm = messagebox.askyesno(
        "Delete",
        "Are you sure you want to delete this task?"
    )

    if confirm:

        deleted_task = tasks.pop(index)

        save_tasks()

        update_listbox()

        update_counter()

        messagebox.showinfo(
            "Deleted",
            f"Task '{deleted_task['title']}' deleted successfully!"
        )

# ---------------- EDIT TASK ---------------- #
def edit_task():

    selected = task_listbox.curselection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Select a task first!"
        )

        return

    index = selected[0]

    task = tasks[index]

    task_entry.delete(0, tk.END)

    task_entry.insert(0, task.get("title", ""))

    due_entry.delete(0, tk.END)

    due_entry.insert(0, task.get("due"))

    priority_var.set(task.get("priority", "Medium"))

    tasks.pop(index)

    save_tasks()

    update_listbox()

    update_counter()

# ---------------- SEARCH TASK ---------------- #
def search_task():

    keyword = search_entry.get().lower().strip()

    filtered_tasks = [
        task for task in tasks
        if keyword in task.get("title", "").lower()
    ]

    update_listbox(filtered_tasks)

# ---------------- SORT BY PRIORITY ---------------- #
def sort_priority():

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    tasks.sort(
        key=lambda x: priority_order.get(
            x.get("priority", "Medium"),
            2
        )
    )

    update_listbox()

    update_counter()

# ---------------- SORT BY DATE ---------------- #
def sort_date():

    def get_date(task):

        due = task.get("due", "01-01-2099")

        try:
            return datetime.strptime(due, "%d-%m-%Y")

        except:
            return datetime.max

    tasks.sort(key=get_date)

    update_listbox()

    update_counter()

# ---------------- DARK/LIGHT THEME ---------------- #
dark_mode = False

def toggle_theme():

    global dark_mode

    dark_mode = not dark_mode

    if dark_mode:

        bg_color = "#2E2E2E"

        fg_color = "white"

        entry_bg = "#1E1E1E"

    else:

        bg_color = "white"

        fg_color = "black"

        entry_bg = "white"

    root.configure(bg=bg_color)

    title_label.configure(bg=bg_color, fg=fg_color)

    task_label.configure(bg=bg_color, fg=fg_color)

    due_label.configure(bg=bg_color, fg=fg_color)

    priority_label.configure(bg=bg_color, fg=fg_color)

    search_label.configure(bg=bg_color, fg=fg_color)

    counter_label.configure(bg=bg_color, fg=fg_color)

    task_entry.configure(
        bg=entry_bg,
        fg=fg_color
    )

    search_entry.configure(
        bg=entry_bg,
        fg=fg_color
    )

# ---------------- REMINDER ---------------- #
def check_reminders():

    today = datetime.today().strftime("%d-%m-%Y")

    for task in tasks:

        if (
            task.get("due") == today and
            not task.get("done", False)
        ):

            messagebox.showinfo(
                "Reminder",
                f"Task Due Today:\n{task.get('title')}"
            )

    root.after(60000, check_reminders)

# ---------------- MAIN WINDOW ---------------- #
root = tk.Tk()

root.title("Advanced To-Do List")

root.geometry("950x780")

root.configure(bg="#2E2E2E")

# ---------------- TITLE ---------------- #
title_label = tk.Label(
    root,
    text="Advanced To-Do List Application",
    font=("Arial", 24, "bold"),
    bg="#2E2E2E",
    fg="white"
)

title_label.pack(pady=15)

# ---------------- TASK TITLE ---------------- #
task_label = tk.Label(
    root,
    text="Task Title",
    bg="#2E2E2E",
    fg="white",
    font=("Arial", 12)
)

task_label.pack()

task_entry = tk.Entry(
    root,
    width=45,
    font=("Arial", 12)
)

task_entry.pack(pady=5)

# ---------------- DUE DATE ---------------- #
due_label = tk.Label(
    root,
    text="Select Due Date",
    bg="#2E2E2E",
    fg="white",
    font=("Arial", 12)
)

due_label.pack()

due_entry = DateEntry(
    root,
    width=42,
    font=("Arial", 12),
    background="#4A90E2",
    foreground="white",
    borderwidth=2,
    date_pattern="dd-mm-yyyy"
)

# Empty date initially
due_entry.delete(0, tk.END)

due_entry.pack(pady=5)

# ---------------- PRIORITY ---------------- #
priority_label = tk.Label(
    root,
    text="Priority",
    bg="#2E2E2E",
    fg="white",
    font=("Arial", 12)
)

priority_label.pack()

priority_var = tk.StringVar(value="Medium")

priority_menu = tk.OptionMenu(
    root,
    priority_var,
    "High",
    "Medium",
    "Low"
)

priority_menu.config(
    width=15,
    font=("Arial", 11)
)

priority_menu.pack(pady=5)

# ---------------- BUTTON STYLE ---------------- #
button_style = {
    "font": ("Arial", 11, "bold"),
    "width": 22,
    "bg": "#4A90E2",
    "fg": "white",
    "activebackground": "#357ABD"
}

# ---------------- BUTTONS ---------------- #
tk.Button(
    root,
    text="➕ Add Task",
    command=add_task,
    **button_style
).pack(pady=5)

tk.Button(
    root,
    text="✔ Complete Task",
    command=complete_task,
    **button_style
).pack(pady=5)

tk.Button(
    root,
    text="🗑 Delete Task",
    command=delete_task,
    **button_style
).pack(pady=5)

tk.Button(
    root,
    text="✏ Edit Task",
    command=edit_task,
    **button_style
).pack(pady=5)

tk.Button(
    root,
    text="⚡ Sort by Priority",
    command=sort_priority,
    **button_style
).pack(pady=5)

tk.Button(
    root,
    text="📅 Sort by Date",
    command=sort_date,
    **button_style
).pack(pady=5)

tk.Button(
    root,
    text="🌙 Toggle Theme",
    command=toggle_theme,
    **button_style
).pack(pady=5)

# ---------------- SEARCH ---------------- #
search_label = tk.Label(
    root,
    text="Search Task",
    bg="#2E2E2E",
    fg="white",
    font=("Arial", 12)
)

search_label.pack(pady=(10, 0))

search_entry = tk.Entry(
    root,
    width=45,
    font=("Arial", 12)
)

search_entry.pack(pady=5)

tk.Button(
    root,
    text="🔍 Search",
    command=search_task,
    **button_style
).pack(pady=5)

# ---------------- TASK FRAME ---------------- #
task_frame = tk.Frame(root)

task_frame.pack(pady=20)

# ---------------- TASK COUNTER ---------------- #
counter_label = tk.Label(
    root,
    text="",
    font=("Arial", 12, "bold"),
    bg="#2E2E2E",
    fg="white"
)

counter_label.pack(pady=5)

# ---------------- SCROLLBAR ---------------- #
scrollbar = tk.Scrollbar(task_frame)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# ---------------- TASK LISTBOX ---------------- #
task_listbox = tk.Listbox(
    task_frame,
    width=110,
    height=15,
    font=("Arial", 11),
    yscrollcommand=scrollbar.set,
    selectbackground="#4A90E2",
    activestyle="none"
)

task_listbox.pack(side=tk.LEFT)

scrollbar.config(command=task_listbox.yview)

# ---------------- KEYBOARD SHORTCUTS ---------------- #
def keyboard_shortcuts(event):

    if event.keysym == "Return":
        add_task()

    elif event.keysym == "Delete":
        delete_task()

root.bind("<Key>", keyboard_shortcuts)

# ---------------- INITIAL LOAD ---------------- #
update_listbox()

update_counter()

# ---------------- START REMINDER ---------------- #
check_reminders()

# ---------------- RUN APPLICATION ---------------- #
root.mainloop()