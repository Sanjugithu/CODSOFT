# todo_list.py
import tkinter as tk
from tkinter import filedialog, ttk
from datetime import datetime
from tkinter import messagebox
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.title("To-Do List App")

# Create a notebook with tabs
tab_control = ttk.Notebook(root)
tab_control.pack(pady=10, expand=True)

# Create tabs for tasks, ongoing tasks, settings, and edit task
tasks_tab = ttk.Frame(tab_control)
ongoing_tasks_tab = ttk.Frame(tab_control)
edit_tab = ttk.Frame(tab_control)
tab_control.add(tasks_tab, text="Tasks")
tab_control.add(ongoing_tasks_tab, text="Ongoing Tasks")
tab_control.add(edit_tab, text="Edit Task")

# Profile tab
profile_tab = ttk.Frame(tab_control)
tab_control.add(profile_tab, text="Profile")

# Create a frame for the profile functionality widgets
profile_frame = tk.Frame(profile_tab)
profile_frame.pack(fill="x", padx=10, pady=10)

# Profile functionality widgets
username_label = tk.Label(profile_frame, text="Username:")
username_label.pack(side=tk.LEFT, padx=5)

username_entry = tk.Entry(profile_frame)
username_entry.pack(side=tk.LEFT, padx=5)

profile_picture_frame = tk.Frame(profile_frame)
profile_picture_frame.pack(side=tk.LEFT, padx=5)

profile_picture_label = tk.Label(profile_picture_frame, text="No Image")
profile_picture_label.pack()

def browse_profile_picture():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
    img = Image.open(file_path)
    img.thumbnail((50, 50))  
    img = ImageTk.PhotoImage(img)
    profile_picture_label.config(image=img)
    profile_picture_label.image = img

profile_picture_button = tk.Button(profile_picture_frame, text="Browse", command=browse_profile_picture)
profile_picture_button.pack()

bio_label = tk.Label(profile_frame, text="Bio:")
bio_label.pack(side=tk.LEFT, padx=5)

bio_text = tk.Text(profile_frame, height=10, width=30)
bio_text.pack(side=tk.LEFT, padx=5)

save_profile_button = tk.Button(profile_frame, text="Save Profile")
save_profile_button.pack()

# Create a treeview for displaying tasks
task_tree = ttk.Treeview(tasks_tab)
task_tree['columns'] = ('Task', 'Due Date', 'Priority')
task_tree.column("#0", width=0, stretch=tk.NO)
task_tree.column("Task", anchor=tk.W, width=200)
task_tree.column("Due Date", anchor=tk.W, width=100)
task_tree.column("Priority", anchor=tk.W, width=50)
task_tree.heading("#0", text='', anchor=tk.W)
task_tree.heading("Task", text='Task', anchor=tk.W)
task_tree.heading("Due Date", text='Due Date', anchor=tk.W)
task_tree.heading("Priority", text='Priority', anchor=tk.W)
task_tree.pack()

# Create a variable to store the selected task's ID
selected_task_id = None

# Create text fields for editing task details
edit_task_name_label = tk.Label(edit_tab, text="Task Name:")
edit_task_name_label.grid(row=0, column=0)
edit_task_name_entry = tk.Entry(edit_tab, width=50)
edit_task_name_entry.grid(row=0, column=1)
edit_due_date_label = tk.Label(edit_tab, text="Due Date:")
edit_due_date_label.grid(row=1, column=0)
edit_due_date_entry = tk.Entry(edit_tab, width=50)
edit_due_date_entry.grid(row=1, column=1)
edit_priority_label = tk.Label(edit_tab, text="Priority:")
edit_priority_label.grid(row=2, column=0)
edit_priority = tk.StringVar(edit_tab)
edit_priority.set("Low")  # default value
priority_options = ["Low", "Medium", "High"]
edit_priority_menu = tk.OptionMenu(edit_tab, edit_priority, *priority_options)
edit_priority_menu.grid(row=2, column=1)

# Create a button to move a task to the "Edit Task" tab
def move_task_to_edit_tab():
    global selected_task_id
    try:
        selected_task_id = task_tree.selection()[0]
        task_details = task_tree.item(selected_task_id, 'values')
        edit_task_name_entry.delete(0, tk.END)
        edit_task_name_entry.insert(0, task_details[0])
        edit_due_date_entry.delete(0, tk.END)
        edit_due_date_entry.insert(0, task_details[1])
        edit_priority.set(task_details[2])  # Set the priority dropdown to the selected task's priority
    except IndexError:
        print("No task selected")

move_task_to_edit_button = tk.Button(tasks_tab, text="Move to Edit Tab", command=move_task_to_edit_tab)
move_task_to_edit_button.pack()

# Create a temporary list to store the task details
task_details_list = []

# Function to update the task details
def update_task_details():
    selected_task_id = task_tree.focus()
    updated_task_name = edit_task_name_entry.get()
 
    # Clear the task_tree widget
    for item in task_tree.get_children():
        task_tree.delete(item)
    
    # Update the task_tree widget with the new list
    for task in task_details_list:
        task_tree.insert('', 'end', values=task)
    
    # Clear the text fields
    edit_task_name_entry.delete(0, tk.END)
    edit_due_date_entry.delete(0, tk.END)
    edit_priority.set("Low")  # Reset the priority dropdown to the default value

# Function to populate the task_details_list
def populate_task_details_list():
    for item in task_tree.get_children():
        task_details_list.append(task_tree.item(item, 'values'))

# Call the populate_task_details_list function when the program starts
populate_task_details_list()

# Create a function to add tasks to the listbox
def add_task():
    task = task_entry.get()
    task_tree.insert(tk.END, task)
    task_entry.delete(0, tk.END)
    update_completed_task_count()

def delete_task():
    try:
        task_index = task_tree.selection()[0]
        task_tree.delete(task_index)
        
        # Remove the task from the Ongoing Tasks listbox
        ongoing_tasks = [ongoing_task for ongoing_task in ongoing_tasks_listbox.get(0, tk.END) if ongoing_task != task_tree.item(task_index, 'values')[0] and not ongoing_task.startswith("[Started] " + task_tree.item(task_index, 'values')[0])]
        ongoing_tasks_listbox.delete(0, tk.END)
        for ongoing_task in ongoing_tasks:
            ongoing_tasks_listbox.insert(tk.END, ongoing_task)
        
        update_completed_task_count()
    except IndexError:
        pass

# Start/Stop task button
def start_stop_task():
    # Get the selected task
    task_index = ongoing_tasks_listbox.curselection()[0]
    task = ongoing_tasks_listbox.get(task_index)

    # Start/Stop the task
    if task.startswith("[Started] "):
        ongoing_tasks_listbox.delete(task_index)
        ongoing_tasks_listbox.insert(task_index, task[10:])
    else:
        ongoing_tasks_listbox.delete(task_index)
        ongoing_tasks_listbox.insert(task_index, "[Started] " + task)

start_stop_task_button = tk.Button(ongoing_tasks_tab, text="Start/Stop Task", command=start_stop_task)
start_stop_task_button.pack()

# Progress bar
ongoing_tasks_progressbar = ttk.Progressbar(ongoing_tasks_tab, orient="horizontal", length=200, mode="determinate")
ongoing_tasks_progressbar.pack()

# Initialize progress bar value
progress_value = 0

# Function to update the progress bar manually
def update_progressbar_manually():
    global progress_value
    if progress_value < 100:
        progress_value += 10
        ongoing_tasks_progressbar['value'] = progress_value

# Create a button to update the progress bar manually
update_progressbar_button = tk.Button(ongoing_tasks_tab, text="Update Progress", command=update_progressbar_manually)
update_progressbar_button.pack()

# Function to reset the progress bar
def reset_progressbar():
    global progress_value
    progress_value = 0
    ongoing_tasks_progressbar['value'] = 0

# Create a button to reset the progress bar
reset_progressbar_button = tk.Button(ongoing_tasks_tab, text="Reset Progress", command=reset_progressbar)
reset_progressbar_button.pack()

# Create a function to save the task list to a file
def save_tasks():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        tasks = task_tree.get(0, tk.END)
        with open(file_path, "w") as file:
            for task in tasks:
                file.write(task + "\n")

# Create a function to load tasks from a file
def load_tasks():
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        task_tree.delete(0, tk.END)
        with open(file_path, "r") as file:
            for line in file:
                task_tree.insert(tk.END, line.strip())
        update_completed_task_count()

#Function to mark tasks as completed
def mark_task_as_completed():
    try:
        selected_task_id = task_tree.selection()[0]
        task_values = task_tree.item(selected_task_id)['values']
        task_name = task_values[0]
        if task_name.startswith("[X] "):
            task_tree.item(selected_task_id, values=(task_name[4:], task_values[1], task_values[2]))
        else:
            task_tree.item(selected_task_id, values=("[X] " + task_name, task_values[1], task_values[2]))
        update_completed_task_count()
    except IndexError:
        pass

def update_completed_task_count():
    completed_tasks = 0
    for task_id in task_tree.get_children():
        task_values = task_tree.item(task_id)['values']
        if task_values[0].startswith("[X] "):
            completed_tasks += 1
    completed_task_count_label.config(text=f"Completed Tasks: {completed_tasks}")

def clear_completed_tasks():
    for task_id in task_tree.get_children():
        task_values = task_tree.item(task_id)['values']
        if task_values[0].startswith("[X] "):
            task_tree.delete(task_id)

def sort_tasks_ascending():
    tasks = task_tree.get_children()
    tasks_list = []
    for task in tasks:
        tasks_list.append(task_tree.item(task)['values'])
    tasks_list.sort()
    task_tree.delete(*tasks)
    for task in tasks_list:
        task_tree.insert('', 'end', values=task)

def sort_tasks_descending():
    tasks = task_tree.get_children()
    tasks_list = []
    for task in tasks:
        tasks_list.append(task_tree.item(task)['values'])
    tasks_list.sort(reverse=True)
    task_tree.delete(*tasks)
    for task in tasks_list:
        task_tree.insert('', 'end', values=task)

    # Ongoing Tasks tab
ongoing_tasks_label = tk.Label(ongoing_tasks_tab, text="Ongoing Tasks:")
ongoing_tasks_label.pack()

ongoing_tasks_listbox = tk.Listbox(ongoing_tasks_tab)
ongoing_tasks_listbox.pack()

    # Function to add a task to the Ongoing Tasks listbox
def add_task_to_ongoing_tasks():
    # Get the selected task from the Tasks tab
    selected_items = task_tree.selection()
    if selected_items:
        task_index = selected_items[0]
        task = task_tree.item(task_index, 'values')[0]
        due_date = task_tree.item(task_index, 'values')[1]
        priority = task_tree.item(task_index, 'values')[2]
        ongoing_tasks_listbox.insert(tk.END, f"{task} - Due: {due_date} - Priority: {priority}")

# Create a button to add a task to the Ongoing Tasks listbox
add_task_to_ongoing_tasks_button = tk.Button(tasks_tab, text="Add to Ongoing Tasks", command=add_task_to_ongoing_tasks)
add_task_to_ongoing_tasks_button.pack()

   # Create the "Add Task" window
add_task_window = tk.Toplevel(root)
add_task_window.title("Add Task")

# Create the task entry field
task_label = tk.Label(add_task_window, text="Task:")
task_label.pack()
task_entry = tk.Entry(add_task_window)
task_entry.pack()

# Create the due date entry field
due_date_label = tk.Label(add_task_window, text="Due Date (YYYY-MM-DD):")
due_date_label.pack()
due_date_entry = tk.Entry(add_task_window)
due_date_entry.pack()

# Create the priority level dropdown menu
priority_label = tk.Label(add_task_window, text="Priority:")
priority_label.pack()
priority_level = tk.StringVar()
priority_level.set("Low")  # Default priority level
priority_menu = tk.OptionMenu(add_task_window, priority_level, "Low", "Medium", "High")
priority_menu.pack()

def add_task_to_tree():
    task = task_entry.get()
    due_date = due_date_entry.get()
    priority = priority_level.get()
    task_tree.insert('', 'end', values=(task, due_date, priority))
    task_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)
    priority_level.set("Low")  # Reset the priority level
    populate_task_details_list()  # Update the task_details_list

# Create a button to add tasks
add_task_button = tk.Button(add_task_window, text="Add Task", command=add_task_to_tree)
add_task_button.pack()

# Create a button for deleting tasks
delete_task_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_task_button.pack()

# Create a button for saving tasks
save_tasks_button = tk.Button(root, text="Save Tasks", command=save_tasks)
save_tasks_button.pack()

# Create a button for loading tasks
load_tasks_button = tk.Button(root, text="Load Tasks", command=load_tasks)
load_tasks_button.pack()

# Create a button for marking tasks as completed
mark_task_button = tk.Button(root, text="Mark as Completed", command=mark_task_as_completed)
mark_task_button.pack()

# Create a button for clearing all completed tasks
clear_completed_tasks_button = tk.Button(root, text="Clear Completed Tasks", command=clear_completed_tasks)
clear_completed_tasks_button.pack()

# Create a button for sorting tasks in ascending order
sort_tasks_ascending_button = tk.Button(root, text="Sort Tasks (Ascending)", command=sort_tasks_ascending)
sort_tasks_ascending_button.pack()

# create a button for sorting tasks in descending order
sort_tasks_descending_button = tk.Button(root, text = "sort Tasks (Descending)", command = sort_tasks_descending)
sort_tasks_descending_button.pack()

# Create a label for displaying the completed task count
completed_task_count_label = tk.Label(root, text="Completed tasks: 0")
completed_task_count_label.pack()

tab_control = ttk.Notebook(root)
tab_control.pack(expand=1, fill="both")

# Create a new tab for editing tasks
edit_tab = ttk.Frame(tab_control)
tab_control.add(edit_tab, text="Edit Task")

# Create a button to save the changes
def save_changes():
    updated_task_name = edit_task_name_entry.get()
    updated_due_date = edit_due_date_entry.get()
    updated_priority = edit_priority.get()
    selected_task = task_tree.selection()[0]
    task_tree.item(selected_task, values=(updated_task_name, updated_due_date, updated_priority))

save_button = tk.Button(edit_tab, text="Save Changes", command=save_changes)
save_button.grid(row=3, column=0, columnspan=2)

# Start the GUI event loop
root.mainloop()
