import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password(length, complexity):
    if complexity == 'low':
        characters = string.ascii_lowercase
    elif complexity == 'medium':
        characters = string.ascii_letters
    elif complexity == 'high':
        characters = string.ascii_letters + string.digits + string.punctuation
    
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def create_password():
    try:
        length = int(length_entry.get())
        complexity = complexity_var.get()
        password = generate_password(length, complexity)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid length")

root = tk.Tk()
root.title("Password Generator")

tk.Label(root, text="Password Generator").grid(row=0, column=0, columnspan=2)

tk.Label(root, text="Length:").grid(row=1, column=0)
length_entry = tk.Entry(root)
length_entry.grid(row=1, column=1)

tk.Label(root, text="Complexity:").grid(row=2, column=0)
complexity_var = tk.StringVar(root)
complexity_var.set("medium")
complexity_option = tk.OptionMenu(root, complexity_var, "low", "medium", "high")
complexity_option.grid(row=2, column=1)

tk.Button(root, text="Generate Password", command=create_password).grid(row=3, column=0, columnspan=2)

tk.Label(root, text="Generated Password:").grid(row=4, column=0)
password_entry = tk.Entry(root, width=40)
password_entry.grid(row=4, column=1)

root.mainloop()
