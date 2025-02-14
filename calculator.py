from tkinter import *

# Create the main window
root = Tk()
root.title("Simple Calculator")
root.geometry("400x500")  # Increased size

# Global variable to store the current expression
expression = ""

# Function to update the expression variable
def update_expression(num):
    global expression
    expression += str(num)
    equation.set(expression)

# Function to evaluate the expression
def evaluate():
    global expression
    try:
        result = eval(expression)
        equation.set(result)
        expression = str(result)
    except:
        equation.set("Error")
        expression = ""

# Function to clear the expression
def clear():
    global expression
    expression = ""
    equation.set("")

# Create the entry field for displaying the equation
equation = StringVar()
entry_field = Entry(root, textvariable=equation, width=40, font=('Arial', 20))  # Increased font size
entry_field.grid(row=0, column=0, columnspan=4, padx=20, pady=20)  # Added padding

# Create the number buttons
button_1 = Button(root, text="1", command=lambda: update_expression(1), width=10, height=3, font=('Arial', 15))
button_1.grid(row=1, column=0, padx=5, pady=5)
button_2 = Button(root, text="2", command=lambda: update_expression(2), width=10, height=3, font=('Arial', 15))
button_2.grid(row=1, column=1, padx=5, pady=5)
button_3 = Button(root, text="3", command=lambda: update_expression(3), width=10, height=3, font=('Arial', 15))
button_3.grid(row=1, column=2, padx=5, pady=5)

button_4 = Button(root, text="4", command=lambda: update_expression(4), width=10, height=3, font=('Arial', 15))
button_4.grid(row=2, column=0, padx=5, pady=5)
button_5 = Button(root, text="5", command=lambda: update_expression(5), width=10, height=3, font=('Arial', 15))
button_5.grid(row=2, column=1, padx=5, pady=5)
button_6 = Button(root, text="6", command=lambda: update_expression(6), width=10, height=3, font=('Arial', 15))
button_6.grid(row=2, column=2, padx=5, pady=5)

button_7 = Button(root, text="7", command=lambda: update_expression(7), width=10, height=3, font=('Arial', 15))
button_7.grid(row=3, column=0, padx=5, pady=5)
button_8 = Button(root, text="8", command=lambda: update_expression(8), width=10, height=3, font=('Arial', 15))
button_8.grid(row=3, column=1, padx=5, pady=5)
button_9 = Button(root, text="9", command=lambda: update_expression(9), width=10, height=3, font=('Arial', 15))
button_9.grid(row=3, column=2, padx=5, pady=5)

button_0 = Button(root, text="0", command=lambda: update_expression(0), width=10, height=3, font=('Arial', 15))
button_0.grid(row=4, column=1, padx=5, pady=5)

# Create the operator buttons
button_add = Button(root, text="+", command=lambda: update_expression("+"), width=10, height=3, font=('Arial', 15))
button_add.grid(row=1, column=3, padx=5, pady=5)
button_subtract = Button(root, text="-", command=lambda: update_expression("-"), width=10, height=3, font=('Arial', 15))
button_subtract.grid(row=2, column=3, padx=5, pady=5)
button_multiply = Button(root, text="*", command=lambda: update_expression("*"), width=10, height=3, font=('Arial', 15))
button_multiply.grid(row=3, column=3, padx=5, pady=5)
button_divide = Button(root, text="/", command=lambda: update_expression("/"), width=10, height=3, font=('Arial', 15))
button_divide.grid(row=4, column=3, padx=5, pady=5)

button_equal = Button(root, text="=", command=evaluate, width=20, height=3, font=('Arial', 15))
button_equal.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

button_clear = Button(root, text="C", command=clear, width=20, height=3, font=('Arial', 15))
button_clear.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

# Start the main loop
root.mainloop()

