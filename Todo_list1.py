import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
from todo_list import ToDoListApp

class ToDoListUI:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(pady=10, expand=True)
        self.create_tabs()

    def create_tabs(self):
        # Create tabs for tasks, ongoing tasks, settings, and edit task
        self.tasks_tab = ttk.Frame(self.tab_control)
        self.ongoing_tasks_tab = ttk.Frame(self.tab_control)
        self.edit_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tasks_tab, text="Tasks")
        self.tab_control.add(self.ongoing_tasks_tab, text="Ongoing Tasks")
        self.tab_control.add(self.edit_tab, text="Edit Task")

        # Profile tab
        self.profile_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.profile_tab, text="Profile")
        self.create_profile_tab()

        # Create a treeview for displaying tasks
        self.task_tree = ttk.Treeview(self.tasks_tab)
        self.task_tree['columns'] = ('Task', 'Due Date', 'Priority')
        self.task_tree.column("#0", width=0, stretch=tk.NO)
        self.task_tree.column("Task", anchor=tk.W, width=200)
        self.task_tree.column("Due Date", anchor=tk.W, width=100)
        self.task_tree.column("Priority", anchor=tk.W, width=50)
        self.task_tree.heading("#0", text='', anchor=tk.W)
        self.task_tree.heading("Task", text='Task', anchor=tk.W)
        self.task_tree.heading("Due Date", text='Due Date', anchor=tk.W)
        self.task_tree.heading("Priority", text='Priority', anchor=tk.W)
        self.task_tree.pack()

        # Ongoing Tasks tab
        self.ongoing_tasks_label = tk.Label(self.ongoing_tasks_tab, text="Ongoing Tasks:")
        self.ongoing_tasks_label.pack()
        self.ongoing_tasks_listbox = tk.Listbox(self.ongoing_tasks_tab)
        self.ongoing_tasks_listbox.pack()

        # Edit Task tab
        self.edit_task_name_label = tk.Label(self.edit_tab, text="Task Name:")
        self.edit_task_name_label.grid(row=0, column=0)
        self.edit_task_name_entry = tk.Entry(self.edit_tab)
        self.edit_task_name_entry.grid(row=0, column=1)

        self.edit_due_date_label = tk.Label(self.edit_tab, text="Due Date:")
        self.edit_due_date_label.grid(row=1, column=0)
        self.edit_due_date_entry = tk.Entry(self.edit_tab)
        self.edit_due_date_entry.grid(row=1, column=1)

        self.edit_priority_label = tk.Label(self.edit_tab, text="Priority:")
        self.edit_priority_label.grid(row=2, column=0)
        self.edit_priority = tk.StringVar()
        self.edit_priority.set("Low")
        self.edit_priority_menu = tk.OptionMenu(self.edit_tab, self.edit_priority, "Low", "Medium", "High")
        self.edit_priority_menu.grid(row=2, column=1)

        self.save_changes_button = tk.Button(self.edit_tab, text="Save Changes")
        self.save_changes_button.grid(row=3, column=0, columnspan=2)

    def create_profile_tab(self):
        # Create a frame for the profile functionality widgets
        profile_frame = tk.Frame(self.profile_tab)
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
        bio_text.pack(side=tk.TOP, padx=5, pady=5)

        save_profile_button = tk.Button(profile_frame, text="Save Profile")
        save_profile_button.pack()

def run(self):
    self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    ui = ToDoListUI(root)
    ui.run()


