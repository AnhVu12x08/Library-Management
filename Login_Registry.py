import tkinter as tk
import re
import json
import bcrypt
import os
from datetime import datetime
import tkinter.messagebox as mb

class UserAuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title('User Authentication')
        self.show_login_window()

    def show_login_window(self):
        self.clear_window()

        tk.Label(self.root, text='Login').grid(row=0, columnspan=2, pady=5)

        tk.Label(self.root, text='Email:').grid(row=1, column=0, pady=2)
        self.login_email = tk.Entry(self.root, width=20)
        self.login_email.grid(row=1, column=1, pady=2)

        tk.Label(self.root, text='Password:').grid(row=2, column=0, pady=2)
        self.login_pw = tk.Entry(self.root, width=20, show='*')
        self.login_pw.grid(row=2, column=1, pady=2)

        tk.Button(self.root, text='Login', command=self.login_event).grid(row=3, columnspan=2, pady=5)
        tk.Button(self.root, text='Register', command=self.show_register_window).grid(row=4, columnspan=2, pady=5)

    def show_register_window(self):
        self.clear_window()

        tk.Label(self.root, text='Register Account').grid(row=0, columnspan=2, pady=5)

        tk.Label(self.root, text='Name:').grid(row=1, column=0, pady=2)
        self.entry_name = tk.Entry(self.root, width=20)
        self.entry_name.grid(row=1, column=1, pady=2)

        tk.Label(self.root, text='Date of birth (YYYY-MM-DD):').grid(row=2, column=0, pady=2)
        self.entry_dob = tk.Entry(self.root, width=20)
        self.entry_dob.grid(row=2, column=1, pady=2)

        tk.Label(self.root, text='Email:').grid(row=3, column=0, pady=2)
        self.entry_email = tk.Entry(self.root, width=20)
        self.entry_email.grid(row=3, column=1, pady=2)

        tk.Label(self.root, text='Password:').grid(row=4, column=0, pady=2)
        self.entry_pw = tk.Entry(self.root, width=20, show='*')
        self.entry_pw.grid(row=4, column=1, pady=2)

        tk.Label(self.root, text='Retype Password:').grid(row=5, column=0, pady=2)
        self.entry_repw = tk.Entry(self.root, width=20, show='*')
        self.entry_repw.grid(row=5, column=1, pady=2)

        tk.Button(self.root, text='Register Account', command=self.register_event).grid(row=6, columnspan=2, pady=5)
        tk.Button(self.root, text='Login', command=self.show_login_window).grid(row=7, columnspan=2, pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def validate_email(self, email):
        regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return re.match(regex, email)

    def validate_age(self, dob):
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age >= 18

    def validate_password(self, password, re_password):
        return password == re_password

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed

    def check_password(self, stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

    def register_event(self):
        name = self.entry_name.get()
        dob_str = self.entry_dob.get()
        email = self.entry_email.get()
        password = self.entry_pw.get()
        re_password = self.entry_repw.get()

        if not all([name, dob_str, email, password, re_password]):
            mb.showerror("Error", "Please fill in all fields.")
            return

        if not self.validate_email(email):
            mb.showerror("Error", "Invalid email format.")
            return

        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d")
            if not self.validate_age(dob):
                mb.showerror("Error", "User must be at least 18 years old.")
                return
        except ValueError:
            mb.showerror("Error", "Invalid date format.")
            return

        if not self.validate_password(password, re_password):
            mb.showerror("Error", "Passwords do not match.")
            return

        users = []
        if os.path.exists('user.json'):
            try:
                with open('user.json', 'r') as file:
                    users = json.load(file)
            except json.JSONDecodeError:
                mb.showerror("Error", "Error reading user data. Please contact support.")
                return

        for user in users:
            if user['email'] == email:
                mb.showerror("Error", "Email already exists.")
                return

        hashed_password = self.hash_password(password)

        new_user = {
            'name': name,
            'dob': dob_str,
            'email': email,
            'password': hashed_password.decode('utf-8')
        }
        users.append(new_user)

        with open('user.json', 'w') as file:
            json.dump(users, file, indent=4)
        mb.showinfo("Success", "User registered successfully")

    def login_event(self):
        email = self.login_email.get()
        password = self.login_pw.get()

        if not all([email, password]):
            mb.showerror("Error", "Please fill in all fields.")
            return

        try:
            with open('user.json', 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            mb.showerror("Error", "No user data found.")
            return

        for user in users:
            if user['email'] == email and self.check_password(user['password'], password):
                mb.showinfo("Success", "Logging in successfully")
                return

        mb.showerror("Error", "Email or Password is wrong")

if __name__ == "__main__":
    root = tk.Tk()
    app = UserAuthApp(root)
    root.mainloop()
