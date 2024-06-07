import tkinter as tk
from tkinter import ttk
import re
import json
import bcrypt
import os
from datetime import datetime
import tkinter.messagebox as mb
import requests

class UserAuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Library Management')
        self.books = []
        self.show_login_window()

    def show_login_window(self):
        self.clear_window()

        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame, text='Login', font=('Arial', 24)).grid(row=0, columnspan=2, pady=10)

        tk.Label(frame, text='Email:', font=('Arial', 16)).grid(row=1, column=0, pady=5, sticky='e')
        self.login_email = tk.Entry(frame, font=('Arial', 16), width=25)
        self.login_email.grid(row=1, column=1, pady=5)

        tk.Label(frame, text='Password:', font=('Arial', 16)).grid(row=2, column=0, pady=5, sticky='e')
        self.login_pw = tk.Entry(frame, font=('Arial', 16), width=25, show='*')
        self.login_pw.grid(row=2, column=1, pady=5)

        tk.Button(frame, text='Login', font=('Arial', 16), command=self.login_event).grid(row=3, columnspan=2, pady=10)

        tk.Label(frame, text='New user?', font=('Arial', 16)).grid(row=4, columnspan=2, pady=10)
        tk.Button(frame, text='Register', font=('Arial', 16), command=self.show_register_window).grid(row=5,
                                                                                                      columnspan=2,
                                                                                                      pady=10)


    def show_register_window(self):
        self.clear_window()

        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame, text='Register Account', font=('Arial', 24)).grid(row=0, columnspan=2, pady=10)

        tk.Label(frame, text='Name:', font=('Arial', 16)).grid(row=1, column=0, pady=5, sticky='e')
        self.entry_name = tk.Entry(frame, font=('Arial', 16), width=25)
        self.entry_name.grid(row=1, column=1, pady=5)

        tk.Label(frame, text='Date of Birth (YYYY-MM-DD):', font=('Arial', 16)).grid(row=2, column=0, pady=5,
                                                                                         sticky='e')
        self.entry_dob = tk.Entry(frame, font=('Arial', 16), width=25)
        self.entry_dob.grid(row=2, column=1, pady=5)

        tk.Label(frame, text='Email:', font=('Arial', 16)).grid(row=3, column=0, pady=5, sticky='e')
        self.entry_email = tk.Entry(frame, font=('Arial', 16), width=25)
        self.entry_email.grid(row=3, column=1, pady=5)

        tk.Label(frame, text='Password:', font=('Arial', 16)).grid(row=4, column=0, pady=5, sticky='e')
        self.entry_pw = tk.Entry(frame, font=('Arial', 16), width=25, show='*')
        self.entry_pw.grid(row=4, column=1, pady=5)

        tk.Label(frame, text='Retype Password:', font=('Arial', 16)).grid(row=5, column=0, pady=5, sticky='e')
        self.entry_repw = tk.Entry(frame, font=('Arial', 16), width=25, show='*')
        self.entry_repw.grid(row=5, column=1, pady=5)

        tk.Button(frame, text='Register Account', font=('Arial', 16), command=self.register_event).grid(row=6,
                                                                                                            columnspan=2,
                                                                                                            pady=10)

        tk.Label(frame, text='Already have an account?', font=('Arial', 16)).grid(row=7, columnspan=2, pady=10)
        tk.Button(frame, text='Login', font=('Arial', 16), command=self.show_login_window).grid(row=8, columnspan=2,
                                                                                                    pady=10)



    def show_user_window(self):
        self.clear_window()
        tk.Label(self.root, text='USER DASHBOARD', font=('Arial', 16)).grid(row=0, columnspan=3, pady=5)

        # Search input field and button
        search_entry = tk.Entry(self.root, width=20)
        search_entry.grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.root, text='Search', command=lambda: self.search_book_event(search_entry.get())).grid(row=1, column=1, padx=5, pady=5)

        # Logout button
        tk.Button(self.root, text='Logout', command=self.logout_event).grid(row=1, column=2, padx=5, pady=5)

        # Create Treeview widget to display book data
        columns = ("Title", "Author", "Year", "Category")
        tree = ttk.Treeview(self.root, columns=columns, show='headings')
        tree.grid(row=2, column=0, columnspan=3, pady=5)

        # Define headings
        for col in columns:
            tree.heading(col, text=col)

        # Load book data from books.json and insert into Treeview
        self.load_books(tree)

    def show_admin_window(self):
        self.clear_window()
        tk.Label(self.root, text='ADMIN DASHBOARD', font=('Arial', 16)).grid(row=0, columnspan=5, padx=5, pady=5)

        # Admin dashboard buttons
        admin_buttons = [
            ('Add Book', self.add_book_event),
            ('Edit Book Info', self.edit_book_event),
            ('Delete Book', self.delete_book_event),
            ('Manage Users', self.manage_users_event),
            ('Logout', self.logout_event)
        ]

        tk.Label(self.root, text='Category:', font=('Arial', 12)).grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.category_entry = tk.Entry(self.root, width=20, font=('Arial', 12))
        self.category_entry.grid(row=3, column=1, padx=5, pady=5)
        tk.Button(self.root, text='Fetch Category Data', command=self.fetch_category_data).grid(row=3, column=2, padx=5,
                                                                                                pady=5)

        for i, (text, command) in enumerate(admin_buttons):
            tk.Button(self.root, text=text, command=command).grid(row=1, column=i, padx=5, pady=5)
        # Create Treeview widget to display book data
        columns = ("Title", "Author", "Year", "Category")
        tree = ttk.Treeview(self.root, columns=columns, show='headings')
        tree.grid(row=2, column=0, columnspan=3, pady=5)

        # Define headings
        for col in columns:
            tree.heading(col, text=col)

        # Load book data from books.json and insert into Treeview
        self.load_books(tree)

    def fetch_category_data(self):
        category = self.category_entry.get().strip()
        if not category:
            mb.showerror("Error", "Please enter a category name.")
            return

        url = f"http://openlibrary.org/subjects/{category}.json"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()

            # Process and format data immediately
            self.format_book_data(data)

            mb.showinfo("Success", "Category data fetched and saved successfully.")
        except requests.RequestException as e:
            mb.showerror("Error",f"Failed to fetch data: {e}")

    def format_book_data(self, data):
        try:
            formatted_works = [
                {
                    "title": work.get("title"),
                    "author": work.get("authors", [{}])[0].get("name") if work.get("authors") else None,
                    "year": work.get("first_publish_year"),
                    "category": data.get("name")
                }
                for work in data.get("works", [])
            ]

            # Open books.json in write mode ('w') to overwrite previous data
            with open("books.json", "w", encoding="utf-8") as f:
                json.dump(formatted_works, f, indent=4, ensure_ascii=False)

        except Exception as e:
            mb.showerror("Error",f"An error occurred while formatting data: {e}")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def validate_email(self, email):
        regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return re.match(regex, email)

    def validate_age(self, dob):
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age >= 5

    def validate_password(self, password, re_password):
        return password == re_password

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def check_password(self, stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

    def register_event(self):
        # Retrieve data from entry fields
        name = self.entry_name.get()
        dob_str = self.entry_dob.get()
        email = self.entry_email.get()
        password = self.entry_pw.get()
        re_password = self.entry_repw.get()

        # Validate form fields
        if not all([name, dob_str, email, password, re_password]):
            mb.showerror("Error", "Please fill in all fields.")
            return

        # Validate email
        if not self.validate_email(email):
            mb.showerror("Error", "Invalid email format.")
            return

        # Validate date of birth
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d")
            if not self.validate_age(dob):
                mb.showerror("Error", "User must be at least 5 years old.")
                return
        except ValueError:
            mb.showerror("Error", "Invalid date format.")
            return

        # Validate password
        if not self.validate_password(password, re_password):
            mb.showerror("Error", "Passwords do not match.")
            return

        # Load existing user data
        users = self.load_users()

        # Check if email already exists
        if any(user['email'] == email for user in users):
            mb.showerror("Error", "Email already exists.")
            return

        # Hash the password
        hashed_password = self.hash_password(password)

        # Create new user and save to file
        new_user = {
            'name': name,
            'dob': dob_str,
            'email': email,
            'password': hashed_password.decode('utf-8'),
            'role': 'user'
        }
        users.append(new_user)
        self.save_users(users)
        mb.showinfo("Success", "User registered successfully")
        self.show_login_window()  # Show login window after successful registration

    def load_users(self):
        """Load users from the JSON file."""
        if os.path.exists('user.json'):
            try:
                with open('user.json', 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                mb.showerror("Error", "Error reading user data. Please contact support.")
                return []
        return []

    def save_users(self, users):
        """Save users to the JSON file."""
        with open('user.json', 'w') as file:
            json.dump(users, file, indent=4)

    def login_event(self):
        # Retrieve data from entry fields
        email = self.login_email.get()
        password = self.login_pw.get()

        # Validate form fields
        if not all([email, password]):
            mb.showerror("Error", "Please fill in all fields.")
            return

        # Load existing user data
        try:
            with open('user.json', 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            mb.showerror("Error", "No user data found.")
            return

        # Check email and password
        for user in users:
            if user['email'] == email and self.check_password(user['password'], password):
                self.current_user = user
                if user.get('role') == 'admin':
                    self.show_admin_window()
                else:
                    self.show_user_window()
                return

        mb.showerror("Error", "Invalid email or password.")

    def load_books(self, tree=None):
        """Load books from the JSON file. Optionally populate a Treeview."""
        if os.path.exists('books.json'):
            try:
                with open('books.json', 'r') as file:
                    self.books = json.load(file)
            except json.JSONDecodeError:
                mb.showerror("Error", "Error reading book data. Please contact support.")
                self.books = [] # Clear self.books in case of error

        # Clear existing data in the tree (whether or not there was an error)
        if tree:
            for i in tree.get_children():
                tree.delete(i)

        # Now safely insert the data (if any)
        if tree:
            for book in self.books:
                tree.insert('', tk.END, values=(book['title'], book['author'], book['year'], book['category']))
    def logout_event(self):
        self.current_user = None
        self.show_login_window()

    def search_book_event(self, search_query):
        # Implement search functionality here
        # You can filter self.books based on search_query
        # and display the results in a new window or update the Treeview
        mb.showinfo("Info", f"Searching for: {search_query}")

    def add_book_event(self):
        self.clear_window()
        tk.Label(self.root, text='ADD NEW BOOK', font=('Arial', 16)).grid(row=0, columnspan=2, pady=5)

        # Book form
        self.create_book_form()

        # Save and Cancel buttons
        tk.Button(self.root, text='Save', command=self.save_book).grid(row=5, columnspan=2, pady=5)
        tk.Button(self.root, text='Cancel', command=self.show_admin_window).grid(row=6, columnspan=2, pady=5)

    def create_book_form(self):
        tk.Label(self.root, text='Title:').grid(row=1, column=0, pady=5, sticky=tk.E)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.root, text='Author:').grid(row=2, column=0, pady=5, sticky=tk.E)
        self.author_entry = tk.Entry(self.root)
        self.author_entry.grid(row=2, column=1, pady=5)

        tk.Label(self.root, text='Publication Year:').grid(row=3, column=0, pady=5, sticky=tk.E)
        self.year_entry = tk.Entry(self.root)
        self.year_entry.grid(row=3, column=1, pady=5)

        tk.Label(self.root, text='Category:').grid(row=4, column=0, pady=5, sticky=tk.E)
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=4, column=1, pady=5)

    def save_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()
        category = self.category_entry.get()

        if not all([title, author, year, category]):
            mb.showerror("Error", "Please fill in all fields.")
            return

        new_book = {
            'title': title,
            'author': author,
            'year': year,
            'category': category
        }

        self.books.append(new_book)
        with open('books.json', 'w') as file:
            json.dump(self.books, file, indent=4)
        mb.showinfo("Success", "Book added successfully")
        self.show_admin_window()

    def edit_book_event(self):
        self.clear_window()
        tk.Label(self.root, text='EDIT BOOK INFO', font=('Arial', 16)).grid(row=0, columnspan=2, pady=5)

        # Create Treeview widget to display book data
        columns = ("ID", "Title", "Author", "Year", "Category")
        self.book_tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.book_tree.grid(row=1, column=0, columnspan=2, pady=5)

        # Define headings
        for col in columns:
            self.book_tree.heading(col, text=col)
            self.book_tree.column(col, width=100)

        # Load book data from books.json and insert into Treeview
        self.load_books()
        for i, book in enumerate(self.books):
            self.book_tree.insert('', tk.END, values=(i, book['title'], book['author'], book['year'], book['category']))

        # Select Book button
        tk.Button(self.root, text='Select Book', command=self.select_book_to_edit).grid(row=2, column=0, pady=5)

        # Cancel button
        tk.Button(self.root, text='Cancel', command=self.show_admin_window).grid(row=2, column=1, pady=5)

    def select_book_to_edit(self):
        selected_item = self.book_tree.selection()
        if not selected_item:
            mb.showerror("Error", "Please select a book to edit.")
            return

        book_id = int(self.book_tree.item(selected_item[0], 'values')[0])
        self.editing_book = self.books[book_id]

        self.clear_window()
        tk.Label(self.root, text='EDIT BOOK DETAILS', font=('Arial', 16)).grid(row=0, columnspan=2, pady=5)

        # Book form with existing data
        self.create_book_form()
        self.title_entry.insert(0, self.editing_book['title'])
        self.author_entry.insert(0, self.editing_book['author'])
        self.year_entry.insert(0, self.editing_book['year'])
        self.category_entry.insert(0, self.editing_book['category'])

        # Save and Cancel buttons
        tk.Button(self.root, text='Save Changes', command=self.save_edited_book).grid(row=5, columnspan=2, pady=5)
        tk.Button(self.root, text='Cancel', command=self.show_admin_window).grid(row=6, columnspan=2, pady=5)

    def save_edited_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()
        category = self.category_entry.get()

        if not all([title, author, year, category]):
            mb.showerror("Error", "Please fill in all fields.")
            return

        # Update the book details
        self.editing_book.update({'title': title, 'author': author, 'year': year, 'category': category})

        # Save the updated books list to the file
        with open('books.json', 'w') as file:
            json.dump(self.books, file, indent=4)

        mb.showinfo("Success", "Book details updated successfully")
        self.show_admin_window()

    def delete_book_event(self):
        self.clear_window()
        tk.Label(self.root, text='DELETE BOOK', font=('Arial', 16)).grid(row=0, columnspan=2, pady=5)

        # Create Treeview widget to display book data
        columns = ("ID", "Title", "Author", "Year", "Category")
        self.book_tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.book_tree.grid(row=1, column=0, columnspan=2, pady=5)

        # Define headings
        for col in columns:
            self.book_tree.heading(col, text=col)
            self.book_tree.column(col, width=100)

        # Load book data from books.json and insert into Treeview
        self.load_books()
        for i, book in enumerate(self.books):
            self.book_tree.insert('', tk.END, values=(i, book['title'], book['author'], book['year'], book['category']))

        # Select Book button
        tk.Button(self.root, text='Select Book', command=self.select_book_to_delete).grid(row=2, column=0, pady=5)

        # Cancel button
        tk.Button(self.root, text='Cancel', command=self.show_admin_window).grid(row=2, column=1, pady=5)

    def select_book_to_delete(self):
        selected_item = self.book_tree.selection()
        if not selected_item:
            mb.showerror("Error", "Please select a book to delete.")
            return

        book_id = int(self.book_tree.item(selected_item[0], 'values')[0])
        if mb.askyesno("Confirm Delete", f"Are you sure you want to delete '{self.books[book_id]['title']}'?"):
            del self.books[book_id]
            with open('books.json', 'w') as file:
                json.dump(self.books, file, indent=4)
            mb.showinfo("Success", "Book deleted successfully")
            self.show_admin_window()  # Refresh the admin window

    def manage_users_event(self):
        self.clear_window()
        tk.Label(self.root, text='MANAGE USERS', font=('Arial', 16)).grid(row=0, columnspan=2, pady=5)

        # Create Treeview widget to display user data
        columns = ("ID", "Name", "Email", "Role")
        self.user_tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.user_tree.grid(row=1, column=0, pady=5)

        # Define headings
        for col in columns:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=100)

        # Load user data from user.json and insert into Treeview
        self.users = self.load_users()
        for i, user in enumerate(self.users):
            self.user_tree.insert('', tk.END, values=(i, user['name'], user['email']))

        # Add User button
        tk.Button(self.root, text='Add User', command=self.add_user_event).grid(row=3, column=0, pady=5)

        # Edit User button
        tk.Button(self.root, text='Edit User', command=self.edit_user_event).grid(row=3, column=1, pady=5)

        # Delete User button
        tk.Button(self.root, text='Delete User', command=self.delete_user_event).grid(row=4, column=0, pady=5)

        # Back to Admin Dashboard button
        tk.Button(self.root, text='Back to Admin Dashboard', command=self.show_admin_window).grid(row=4, column=1, pady=5)

    def add_user_event(self):
        self.clear_window()
        tk.Label(self.root, text='ADD NEW USER', font=('Arial', 16)).grid(row=0, columnspan=2, pady=5)

        # User form
        self.create_user_form()

        # Save and Cancel buttons
        tk.Button(self.root, text='Save', command=self.save_user).grid(row=7, columnspan=2, pady=5)  # Moved to row 7
        tk.Button(self.root, text='Cancel', command=self.manage_users_event).grid(row=8, columnspan=2, pady=5)

    def create_user_form(self):
        tk.Label(self.root, text='Name:').grid(row=1, column=0, pady=5, sticky=tk.E)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.root, text='Date of birth (YYYY-MM-DD):').grid(row=2, column=0, pady=5, sticky=tk.E)
        self.dob_entry = tk.Entry(self.root)
        self.dob_entry.grid(row=2, column=1, pady=5)

        tk.Label(self.root, text='Email:').grid(row=3, column=0, pady=5, sticky=tk.E)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=3, column=1, pady=5)

        tk.Label(self.root, text='Password:').grid(row=4, column=0, pady=5, sticky=tk.E)
        self.pw_entry = tk.Entry(self.root, show='*')
        self.pw_entry.grid(row=4, column=1, pady=5)

        tk.Label(self.root, text='Retype Password:').grid(row=5, column=0, pady=5, sticky=tk.E)
        self.repw_entry = tk.Entry(self.root, show='*')
        self.repw_entry.grid(row=5, column=1, pady=5)

    def save_user(self):
        name = self.name_entry.get()
        dob_str = self.dob_entry.get()
        email = self.email_entry.get()
        password = self.pw_entry.get()
        re_password = self.repw_entry.get()

        # Validate form fields
        if not all([name, dob_str, email, password, re_password]):
            mb.showerror("Error", "Please fill in all fields.")
            return

        # Validate email
        if not self.validate_email(email):
            mb.showerror("Error", "Invalid email format.")
            return

        # Validate date of birth
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d")
            if not self.validate_age(dob):
                mb.showerror("Error", "User must be at least 5 years old.")
                return
        except ValueError:
            mb.showerror("Error", "Invalid date format.")
            return

        # Validate password
        if not self.validate_password(password, re_password):
            mb.showerror("Error", "Passwords do not match.")
            return

        # Check if email already exists
        if any(user['email'] == email for user in self.users):
            mb.showerror("Error", "Email already exists.")
            return

        # Hash the password
        hashed_password = self.hash_password(password)

        # Create new user and save to file
        new_user = {
            'name': name,
            'dob': dob_str,
            'email': email,
            'password': hashed_password.decode('utf-8'),
            'role': 'user'
        }
        self.users.append(new_user)
        self.save_users(self.users)
        mb.showinfo("Success", "User added successfully")
        self.manage_users_event() # refresh the manage users window after adding a new user

    def edit_user_event(self):
        selected_item = self.user_tree.selection()
        if not selected_item:
            mb.showerror("Error", "Please select a user to edit.")
            return

        user_id = int(self.user_tree.item(selected_item[0], 'values')[0])
        self.editing_user = self.users[user_id]

        self.clear_window()
        tk.Label(self.root, text='EDIT USER DETAILS', font=('Arial', 16)).grid(row=0, columnspan=2, pady=5)

        # User form with existing data
        self.create_user_form()
        self.name_entry.insert(0, self.editing_user['name'])
        self.dob_entry.insert(0, self.editing_user['dob'])
        self.email_entry.insert(0, self.editing_user['email'])
        # We don't show password in edit form
        # self.pw_entry.insert(0, self.editing_user['password'])
        # self.repw_entry.insert(0, self.editing_user['password'])

        # Save and Cancel buttons
        tk.Button(self.root, text='Save Changes', command=self.save_edited_user).grid(row=5, columnspan=2, pady=5)
        tk.Button(self.root, text='Cancel', command=self.manage_users_event).grid(row=6, columnspan=2, pady=5)

    def save_edited_user(self):
        name = self.name_entry.get()
        dob_str = self.dob_entry.get()
        email = self.email_entry.get()
        # We don't get password from edit form

        # Validate form fields
        if not all([name, dob_str, email]):
            mb.showerror("Error", "Please fill in all fields.")
            return

        # Validate email
        if not self.validate_email(email):
            mb.showerror("Error", "Invalid email format.")
            return

        # Validate date of birth
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d")
            if not self.validate_age(dob):
                mb.showerror("Error", "User must be at least 5 years old.")
                return
        except ValueError:
            mb.showerror("Error", "Invalid date format.")
            return

        # Update the user details
        self.editing_user.update({'name': name, 'dob': dob_str, 'email': email})

        # Save the updated users list to the file
        with open('user.json', 'w') as file:
            json.dump(self.users, file, indent=4)

        mb.showinfo("Success", "User details updated successfully")
        self.manage_users_event()

    def delete_user_event(self):
        selected_item = self.user_tree.selection()
        if not selected_item:
            mb.showerror("Error", "Please select a user to delete.")
            return

        user_id = int(self.user_tree.item(selected_item[0], 'values')[0])
        if mb.askyesno("Confirm Delete", f"Are you sure you want to delete '{self.users[user_id]['name']}'?"):
            del self.users[user_id]
            with open('user.json', 'w') as file:
                json.dump(self.users, file, indent=4)
            mb.showinfo("Success", "User deleted successfully")
            self.manage_users_event()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    app = UserAuthApp(root)
    root.mainloop()