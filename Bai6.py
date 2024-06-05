import tkinter as tk
import re
import json
import bcrypt
from datetime import datetime
import tkinter.messagebox as mb

root = tk.Tk()
root.title('Login')

def check_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

def submitevent():
    # Retrieve data from entry fields
    email = entry_email.get()
    password = entry_pw.get()

    # Check if all fields are filled
    if not all([email, password]):
        mb.showerror("Error", "Please fill in all fields.")
        return

    try:
        with open('user.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        mb.showerror("Error", "No user data found.")
        return

    # Check if email and password are correct
    for user in users:
        if user['email'] == email and check_password(user['password'], password):
            mb.showinfo("Success", "Logging in successfully")
            return

    mb.showerror("Error", "Email or Password is wrong")

label_email = tk.Label(root, text='Email:')
label_email.grid(row=0, column=0, pady=2)
entry_email = tk.Entry(root, width=20)
entry_email.grid(row=0, column=1, pady=2)

label_pw = tk.Label(root, text='Password:')
label_pw.grid(row=1, column=0, pady=2)
entry_pw = tk.Entry(root, width=20, show='*')
entry_pw.grid(row=1, column=1, pady=2)

submit = tk.Button(root, text='Login', command=submitevent)
submit.grid(row=2, columnspan=2, pady=2)

label = tk.Label(root, text="")
label.grid(row=3, columnspan=2, pady=5)

root.mainloop()
