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
        self.root.title('Library Management')
        self.current_user = None
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
        tk.Label(self.root, text='You dont have account?').grid(row=4, columnspan = 2, pady =5)
        tk.Button(self.root, text='Register', command=self.show_register_window).grid(row=5, columnspan=2, pady=5)

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
        tk.Label(self.root, text='You wanna login?').grid(row=7, columnspan = 2, pady =5)
        tk.Button(self.root, text='Login', command=self.show_login_window).grid(row=8, columnspan=2, pady=5)

    def show_user_window(self):
        self.clear_window()
        tk.Label(self.root, text='USER DASHBOARD', font=('Arial', 16)).grid(row=0, columnspan=2, pady=5)

        # Search input field and button in one row
        search_entry = tk.Entry(self.root, width=20)
        search_entry.grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.root, text='Search', command=lambda: self.search_book_event(search_entry.get())).grid(row=1,
                                                                                                             column=1,
                                                                                                             padx=5,
                                                                                                             pady=5)

        # Logout button
        tk.Button(self.root, text='Logout', command=self.logout_event).grid(row=1, column=2, padx=5, pady=5)

        # Data display below buttons
        # Replace the following placeholder labels with actual data widgets (e.g., Listbox, Treeview)
        tk.Label(self.root, text='Book Data 1').grid(row=2, column=0, pady=5)
        tk.Label(self.root, text='Book Data 2').grid(row=3, column=0, pady=5)
        tk.Label(self.root, text='Book Data 3').grid(row=4, column=0, pady=5)

    def show_admin_window(self):
        self.clear_window()
        tk.Label(self.root, text='ADMIN DASHBOARD', font=('Arial', 16)).grid(row=0, columnspan=5, padx=5, pady=5)

        # Add Book button
        tk.Button(self.root, text='Add Book', command=self.add_book_event).grid(row=1, column=0, padx=5, pady=5)

        # Edit Book Info button
        tk.Button(self.root, text='Edit Book Info', command=self.edit_book_event).grid(row=1, column=1, padx=5, pady=5)

        # Delete Book button
        tk.Button(self.root, text='Delete Book', command=self.delete_book_event).grid(row=1, column=2, padx=5, pady=5)

        # Manage Users button
        tk.Button(self.root, text='Manage Users', command=self.manage_users_event).grid(row=1, column=3, padx=5, pady=5)

        # Logout button
        tk.Button(self.root, text='Logout', command=self.logout_event).grid(row=1, column=4, padx=5, pady=5)

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
            'password': hashed_password.decode('utf-8'),
            'role': 'user'
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
                self.current_user = user
                if user.get('role') == 'admin':
                    self.show_admin_window()
                else:
                    self.show_user_window()
                return

        mb.showerror("Error", "Email or Password is wrong")

    def logout_event(self):
        self.current_user = None
        self.show_login_window()

    # Placeholder methods for book management and user management
    def search_book_event(self):
        mb.showinfo("Info", "Search Book Functionality")

    def view_book_info_event(self):
        mb.showinfo("Info", "View Book Info Functionality")

    def add_book_event(self):
        mb.showinfo("Info", "Add Book Functionality")

    def edit_book_event(self):
        mb.showinfo("Info", "Edit Book Info Functionality")

    def delete_book_event(self):
        mb.showinfo("Info", "Delete Book Functionality")

    def manage_users_event(self):
        mb.showinfo("Info", "Manage Users Functionality")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")
    app = UserAuthApp(root)
    root.mainloop()


