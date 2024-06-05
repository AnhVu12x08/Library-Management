import tkinter as tk
import re
import json
import os
from datetime import datetime
import tkinter.messagebox as mb
import bcrypt

root = tk.Tk()
root.title('Registry Account')

def validate_email(email):
    regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return re.match(regex, email)

def validate_age(dob):
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age >= 18

def validate_password(password, re_password):
    return password == re_password

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def submitevent():
    # Retrieve data from entry fields
    name = entry_name.get()
    dob_str = entry_dob.get()
    email = entry_email.get()
    password = entry_pw.get()
    re_password = entry_repw.get()

    # Check if all fields are filled
    if not all([name, dob_str, email, password, re_password]):
        mb.showerror("Error", "Please fill in all fields.")
        return

    # Validate email format
    if not validate_email(email):
        mb.showerror("Error", "Invalid email format.")
        return

    # Validate age
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
        if not validate_age(dob):
            mb.showerror("Error", "User must be at least 18 years old.")
            return
    except ValueError:
        mb.showerror("Error", "Invalid date format.")
        return

    # Validate password match
    if not validate_password(password, re_password):
        mb.showerror("Error", "Passwords do not match.")
        return

    # Load existing user data from file
    users = []
    if os.path.exists('user.json'):
        try:
            with open('user.json', 'r') as file:
                users = json.load(file)
        except json.JSONDecodeError:
            mb.showerror("Error", "Error reading user data. Please contact support.")
            return

    # Check if email already exists
    for user in users:
        if user['email'] == email:
            mb.showerror("Error", "Email already exists.")
            return

    # Hash the password
    hashed_password = hash_password(password)

    # Add new user to user list
    new_user = {
        'name': name,
        'dob': dob_str,
        'email': email,
        'password': hashed_password.decode('utf-8')  # Store as string for JSON serialization
    }
    users.append(new_user)

    # Save updated user data to file
    with open('user.json', 'w') as file:
        json.dump(users, file, indent=4)
    mb.showinfo("Success", "User registered successfully")

label_name = tk.Label(root, text='Name:')
label_name.grid(row=0, column=0, pady=2)
entry_name = tk.Entry(root, width=20)
entry_name.grid(row=0, column=1, pady=2)

label_dob = tk.Label(root, text='Date of birth (YYYY-MM-DD):')
label_dob.grid(row=1, column=0, pady=2)
entry_dob = tk.Entry(root, width=20)
entry_dob.grid(row=1, column=1, pady=2)

label_email = tk.Label(root, text='Email:')
label_email.grid(row=2, column=0, pady=2)
entry_email = tk.Entry(root, width=20)
entry_email.grid(row=2, column=1, pady=2)

label_pw = tk.Label(root, text='Password:')
label_pw.grid(row=3, column=0, pady=2)
entry_pw = tk.Entry(root, width=20, show='*')
entry_pw.grid(row=3, column=1, pady=2)

label_repw = tk.Label(root, text='Retype Password:')
label_repw.grid(row=4, column=0, pady=2)
entry_repw = tk.Entry(root, width=20, show='*')
entry_repw.grid(row=4, column=1, pady=2)

submit = tk.Button(root, text='Register Account', command=submitevent)
submit.grid(row=5, columnspan=2, pady=2)

label = tk.Label(root, text="")
label.grid(row=6, columnspan=2, pady=5)

root.mainloop()
