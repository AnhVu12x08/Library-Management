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
        self.users = []  # Initialize users list
        self.editing_book = None
        self.editing_user = None
        self.current_user = None
        self.show_login_window()

    def show_login_window(self):
        self.clear_window()

        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=420, height= 400)

        tk.Label(frame, text='Login', font=('Arial', 24)).grid(row=0, columnspan=2, pady=10)

        tk.Label(frame, text='Email:', font=('Arial', 16)).grid(row=1, column=0, pady=5, sticky='e')
        self.login_email = tk.Entry(frame, font=('Arial', 16), width=25)
        self.login_email.grid(row=1, column=1, pady=5)

        tk.Label(frame, text='Password:', font=('Arial', 16)).grid(row=2, column=0, pady=5, sticky='e')
        self.login_pw = tk.Entry(frame, font=('Arial', 16), width=25, show='*')
        self.login_pw.grid(row=2, column=1, pady=5)

        tk.Button(frame, text='Login', font=('Arial', 16), command=self.login_event).grid(row=3, columnspan=2, pady=10)

        ttk.Separator(frame, orient='horizontal').grid(row=4, columnspan=3, sticky='ew', pady=10)

        tk.Label(frame, text='New user?', font=('Arial', 16)).grid(row=5, columnspan=2, pady=10)
        tk.Button(frame, text='Register', font=('Arial', 16), command=self.show_register_window).grid(row=6,
                                                                                                      columnspan=2,
                                                                                                      pady=10)

    def show_register_window(self):
        self.clear_window()

        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER,height=500, width=600)

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
        ttk.Separator(frame, orient='horizontal').grid(row=7, columnspan=3, sticky='ew', pady=10)


        tk.Label(frame, text='Already have an account?', font=('Arial', 16)).grid(row=8, columnspan=2, pady=10)
        tk.Button(frame, text='Login', font=('Arial', 16), command=self.show_login_window).grid(row=9, columnspan=2,
                                                                                                pady=10)

    def show_user_window(self):
        self.clear_window()

        # User Dashboard Label
        tk.Label(self.root, text='USER DASHBOARD', font=('Arial', 24, 'bold'), fg='white', bg='#58A4B0', borderwidth=2,
                 relief='solid').grid(row=0, column=0, columnspan=3, pady=20, padx=10, sticky='nsew')

        # Search input field
        self.search_entry = tk.Entry(self.root, width=30, font=('Arial', 13))
        self.search_entry.place(x=20, y=70, width=300, height=30)  # Adjust x, y coordinates as needed

        # Search button
        search_button = tk.Button(self.root, text='Search', command=self.search_book_event, font=('Arial', 13))
        search_button.place(x=350, y=70, width=100, height=30)  # Adjust x, y coordinates as needed

        # Logout button
        logout_button = tk.Button(self.root, text='Logout', command=self.logout_event, font=('Arial', 13))
        logout_button.place(x=1000, y=70, width=100, height=30)  # Adjust x, y coordinates as needed

        # Create Treeview widget to display book data
        columns = ("Stt", "Title", "Author", "Year", "Category")
        self.book_tree = ttk.Treeview(self.root, columns=columns, show='headings', height=10)
        self.book_tree.grid(row=3, column=0, columnspan=3, pady=20, padx=20, sticky='nsew')

        # Define headings and set column widths
        for col in columns:
            self.book_tree.heading(col, text=col)
            self.book_tree.column(col, width=150)

        # Configure grid columns for equal weight
        self.root.grid_rowconfigure(3, weight=1)  # Make row 3 (containing Treeview) expandable
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        # Load book data from books.json and insert into Treeview
        self.load_books(self.book_tree)

    def show_admin_window(self):
        self.clear_window()
        tk.Label(self.root, text='ADMIN DASHBOARD', font=('Arial', 24, 'bold'), fg='white', bg='#58A4B0',
                 borderwidth=2, relief='solid').grid(row=0, columnspan=5, padx=10, pady=10, sticky='ew')


        add_button = tk.Button(self.root, text='Add Book', command= self.add_book_event, font=('Arial', 13))
        add_button.place(x=30, y=70, width=130, height=30)  # Adjust x, y coordinates as needed

        edit_button = tk.Button(self.root, text='Edit Book Info', command=self.edit_book_event, font=('Arial', 13))
        edit_button.place(x=180, y=70, width=130, height=30)  # Adjust x, y coordinates as needed

        delete_button = tk.Button(self.root, text='Delete Book', command=self.delete_book_event, font=('Arial', 13))
        delete_button.place(x=330, y=70, width=130, height=30)  # Adjust x, y coordinates as needed

        manage_button = tk.Button(self.root, text='Manage Users', command=self.manage_users_event, font=('Arial', 13))
        manage_button.place(x=480, y=70, width=130, height=30)  # Adjust x, y coordinates as needed

        logout_button = tk.Button(self.root, text='Logout', command=self.logout_event, font=('Arial', 13))
        logout_button.place(x=1000, y=70, width=130, height=30)  # Adjust x, y coordinates as needed

        # Category fetching
        tk.Label(self.root, text='Category:', font=('Arial', 12)).place(x=30, y=370, width=130, height=30)
        self.category_entry = tk.Entry(self.root, width=30, font=('Arial', 12))
        self.category_entry.place(x=180, y=370, width=300, height=30)
        tk.Button(self.root, text='Fetch Category Data', command=self.fetch_category_data).place(x=500, y=370,width=130, height=30)
        # Admin buttons

        columns = ("Stt", "Title", "Author", "Year", "Category")
        self.book_tree = ttk.Treeview(self.root, columns=columns, show='headings', height=10)
        self.book_tree.place(x=30, y=120)

        # Define headings and set column widths
        for col in columns:
            self.book_tree.heading(col, text=col)
            self.book_tree.column(col, width=250)

        # Configure grid columns for equal weight
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        # Load book data from books.json and insert into Treeview
        self.load_books(self.book_tree)


    def clear_and_create_widgets(self, title, command_select, command_cancel):
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry)):  # Include tk.Entry
                widget.destroy()

        # Re-create the label and buttons
        tk.Label(self.root, text=title, font=('Arial', 24, 'bold'), fg='white', bg='#58A4B0', borderwidth=2,
                 relief='solid').grid(row=0, columnspan=2, pady=5, padx=20, sticky='n')
        tk.Button(self.root, text='Select Book',font=('Arial',13), command=command_select).grid(row=5, column=0, pady=5)
        tk.Button(self.root, text='Cancel', font=('Arial',13), command=command_cancel).grid(row=5, column=1, pady=5)

        # Update the Treeview
        self.book_tree.delete(*self.book_tree.get_children())
        self.load_books(self.book_tree)

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

            # Update the Treeview after fetching data
            self.clear_window()
            self.show_admin_window()  # Refresh the admin window to display new data

            mb.showinfo("Success", "Category data fetched and saved successfully.")
        except requests.RequestException as e:
            mb.showerror("Error", f"Failed to fetch data: {e}")

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

            # Append new data to existing data in books.json
            self.append_to_json("books.json", formatted_works)

        except Exception as e:
            mb.showerror("Error", f"An error occurred while formatting data: {e}")

    def append_to_json(self, file_path, new_data):
        try:
            with open(file_path, "r+", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []  # File is empty or not valid JSON
                f.seek(0)  # Move pointer to the beginning of the file
                json.dump(data + new_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            mb.showerror("Error", f"An error occurred while appending data: {e}")

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

    #def is_valid_year(year_str):
    #    if len(year_str) == 4 and year_str.isdigit():
    #        return True
    #    return False

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
        # label = tk.Label(self.root, text = 'debg')
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

    def load_books(self, tree):
        try:
            with open("books.json", "r", encoding="utf-8") as f:
                self.books = json.load(f)

                # Clear existing data in the Treeview
                tree.delete(*tree.get_children())

                # Insert new data into the Treeview
                for i, book in enumerate(self.books):
                    tree.insert('', tk.END, values=(i, book['title'], book['author'], book['year'], book['category']))
        except Exception as e:
            mb.showerror("Error", f"An error occurred while loading books: {e}")

    def logout_event(self):
        self.current_user = None
        self.show_login_window()


    def search_book_event(self):
        search_query = self.search_entry.get().lower()  # Lấy nội dung tìm kiếm và chuyển về chữ thường
        if not search_query:
            # Nếu không có nội dung tìm kiếm, hiển thị lại toàn bộ danh sách sách
            self.update_treeview(self.book_tree)  # Assuming you want to update the Treeview
            return

        matching_books = []
        for book in self.books:
            # Kiểm tra nội dung tìm kiếm có tồn tại trong title, author, year, category hay không
            if (
                    search_query in book['title'].lower()
                    or search_query in book['author'].lower()
                    or search_query in str(book['year'])
                    or search_query in book['category'].lower()
            ):
                matching_books.append(book)

        # Xóa dữ liệu hiện tại trong Treeview và hiển thị kết quả tìm kiếm
        self.book_tree.delete(*self.book_tree.get_children())
        for i, book in enumerate(matching_books):
            self.book_tree.insert('', tk.END, values=(i, book['title'], book['author'], book['year'], book['category']))

    def update_treeview(self, tree):
        self.book_tree.delete(*self.book_tree.get_children())

        for i, book in enumerate(self.books):
            tree.insert('', tk.END, values=(i, book['title'], book['author'], book['year'], book['category']))

    def add_book_event(self):
        self.clear_window()
        tk.Label(self.root, text='ADD NEW BOOK', font=('Arial', 24, 'bold'), fg='white', bg='#58A4B0', borderwidth=2,
                 relief='solid').grid(row=0, columnspan=2, pady=5, padx=20, sticky='n')

        # Book form
        self.create_book_form()
        button_font = ('Arial',13)
        # Save and Cancel buttons
        tk.Button(self.root, text='Save',font=button_font, command=self.save_book, height=1,width=10).grid(row=7, columnspan=2, pady=5)
        tk.Button(self.root, text='Cancel',font=button_font, command=self.show_admin_window).grid(row=8, columnspan=2, pady=5)

    def create_book_form(self):
        # Configure grid weight for centering
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Define font and padding
        label_font = ('Arial', 14)
        entry_font = ('Arial', 14)
        pady = 10
        padx = 20

        tk.Label(self.root, text='Title:',font=label_font).grid(row=1, column=0, pady=pady, padx=padx, sticky=tk.E)
        self.title_entry = tk.Entry(self.root, font=entry_font)
        self.title_entry.grid(row=1, column=1, pady=pady,sticky=tk.W )

        tk.Label(self.root, text='Author:',font=label_font).grid(row=2, column=0, pady=pady, padx=padx, sticky=tk.E)
        self.author_entry = tk.Entry(self.root,font=entry_font)
        self.author_entry.grid(row=2, column=1, pady=pady,sticky=tk.W)

        tk.Label(self.root, text='Publication Year:',font=label_font).grid(row=3, column=0,  pady=pady, padx=padx, sticky=tk.E)
        self.year_entry = tk.Entry(self.root,font=entry_font)
        self.year_entry.grid(row=3, column=1, pady=pady,sticky=tk.W)

        tk.Label(self.root, text='Category:',font=label_font).grid(row=4, column=0, pady=pady, padx=padx, sticky=tk.E)
        self.category_entry = tk.Entry(self.root,font=entry_font)
        self.category_entry.grid(row=4, column=1, pady=pady,sticky=tk.W)

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

        # Append new book to existing data in books.json
        self.append_to_json("books.json", [new_book])

        mb.showinfo("Success", "Book added successfully")
        self.show_admin_window()

    def append_to_json(self, file_path, new_data):
        try:
            with open(file_path, "r+", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []  # File is empty or not valid JSON
                f.seek(0)  # Move pointer to the beginning of the file
                json.dump(data + new_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            mb.showerror("Error", f"An error occurred while appending data: {e}")

    def edit_book_event(self):
        self.clear_and_create_widgets('EDIT BOOK INFO', self.select_book_to_edit, self.show_admin_window)

    def select_book_to_edit(self):
        selected_item = self.book_tree.selection()
        if not selected_item:
            mb.showerror("Error", "Please select a book to edit.")
            return

        book_id = int(self.book_tree.item(selected_item[0], 'values')[0])
        self.editing_book = self.books[book_id]

        self.clear_window()

        # Display edit book form
        tk.Label(self.root, text='EDIT BOOK DETAILS', font=('Arial', 24, 'bold'), fg='white', bg='#58A4B0', borderwidth=2,
                 relief='solid').grid(row=0, columnspan=2, pady=5)

        # Create book form with existing data
        self.create_book_form()
        self.title_entry.insert(0, self.editing_book['title'])
        self.author_entry.insert(0, self.editing_book['author'])
        self.year_entry.insert(0, self.editing_book['year'])
        self.category_entry.insert(0, self.editing_book['category'])

        button_font = ('Arial', 13)

        # Save and Cancel buttons
        tk.Button(self.root, text='Save Changes', command=self.save_edited_book,height= 1, width=18, font= button_font).place(x=500, y=280)
        tk.Button(self.root, text='Cancel', command=self.show_admin_window, height= 1, font= button_font).place(x=550, y=330)

    def save_edited_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()
        category = self.category_entry.get()

        if not all([title, author, year, category]):
            mb.showerror("Error", "Please fill in all fields.")
            return

        # Update the book in the self.books list
        self.editing_book['title'] = self.title_entry.get()
        self.editing_book['author'] = self.author_entry.get()
        self.editing_book['year'] = int(self.year_entry.get())  # Assuming year is an integer
        self.editing_book['category'] = self.category_entry.get()

        # Save the updated books list to the file
        with open('books.json', 'w') as file:
            json.dump(self.books, file, indent=4)

        mb.showinfo('Success', 'Book edit successfully')
        self.show_admin_window()

    # --- Delete Book Functionality ---

    def delete_book_event(self):
        self.clear_and_create_widgets('DELETE BOOK', self.select_book_to_delete, self.show_admin_window)

    def select_book_to_delete(self):
        selected_item = self.book_tree.selection()
        if not selected_item:
            mb.showerror("Error", "Please select a book to delete.")
            return

        book_id = int(self.book_tree.item(selected_item[0], 'values')[0])
        if mb.askyesno("Confirm Delete", f"Are you sure you want to delete '{self.books[book_id]['title']}'?"):
            del self.books[book_id]
            # Update the book list in books.json
            self.update_books_json()
            mb.showinfo("Success", "Book deleted successfully")
            self.show_admin_window()  # Refresh the admin window

    def update_books_json(self):
        # Update the books.json file
        try:
            with open("books.json", "w", encoding="utf-8") as f:
                json.dump(self.books, f, indent=4, ensure_ascii=False)
        except Exception as e:
            mb.showerror("Error", f"An error occurred while updating books.json: {e}")

    # --- Manage Users Functionality ---

    def manage_users_event(self):
        self.clear_window()

        # Title
        title_label = tk.Label(self.root, text='MANAGE USERS', font=('Arial', 24, 'bold'), fg='white', bg='#58A4B0',
                               borderwidth=2, relief='solid')
        title_label.grid(row=0, columnspan=2, pady=5, padx=20, sticky='n')

        # Create Treeview widget to display user data
        columns = ("Stt", "Name", "Email", "Role")
        self.user_tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.user_tree.grid(row=1, column=0, columnspan=2, pady=20, padx=20)

        # Define headings
        for col in columns:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=200)

        # Load user data from user.json and insert into Treeview
        self.users = self.load_users()
        for i, user in enumerate(self.users):
            self.user_tree.insert('', tk.END, values=(i, user['name'], user['email'], user['role']))

        # Buttons
        button_font = ('Arial', 13)
        button_padx = 20
        button_pady = 5

        add_button = tk.Button(self.root, text='Add User', font=button_font, command=self.add_user_event, height = 1, width = 22)
        add_button.grid(row=2, column=0, pady=button_pady, padx=button_padx, sticky='e')

        edit_button = tk.Button(self.root, text='Edit User', font=button_font, command=self.edit_user_event, height = 1, width = 22)
        edit_button.grid(row=2, column=1, pady=button_pady, padx=button_padx, sticky='w')

        delete_button = tk.Button(self.root, text='Delete User', font=button_font, command=self.delete_user_event, height = 1, width = 22)
        delete_button.grid(row=3, column=0, pady=button_pady, padx=button_padx, sticky='e')

        back_button = tk.Button(self.root, text='Back to Admin Dashboard', font=button_font,
                                command=self.show_admin_window, height = 1, width = 22)
        back_button.grid(row=3, column=1, pady=button_pady, padx=button_padx, sticky='w')

    def add_user_event(self):
        self.clear_window()
        tk.Label(self.root, text='ADD NEW USER', font=('Arial', 24, 'bold'), fg='white', bg='#58A4B0', borderwidth=2,
                 relief='solid').grid(row=0, columnspan=2, pady=5, padx=20, sticky='n')

        # User form
        self.create_user_form()
        button_font = ('Arial', 13)

        # Save and Cancel buttons
        tk.Button(self.root, text='Save', font= button_font, command=self.save_user, height=1, width=10).grid(row=7, columnspan=2, pady=5)  # Moved to row 7
        tk.Button(self.root, text='Cancel', font = button_font, command=self.manage_users_event).grid(row=8, columnspan=2, pady=5)

    def create_user_form(self):
        # Configure grid weight for centering
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Define font and padding
        label_font = ('Arial', 14)
        entry_font = ('Arial', 14)
        pady = 10
        padx = 20

        # Name
        tk.Label(self.root, text='Name:', font=label_font).grid(row=1, column=0, pady=pady, padx=padx, sticky=tk.E)
        self.name_entry = tk.Entry(self.root, font=entry_font)
        self.name_entry.grid(row=1, column=1, pady=pady, padx=padx, sticky=tk.W)

        # Date of birth
        tk.Label(self.root, text='Date of birth (YYYY-MM-DD):', font=label_font).grid(row=2, column=0, pady=pady, padx=padx, sticky=tk.E)
        self.dob_entry = tk.Entry(self.root, font=entry_font)
        self.dob_entry.grid(row=2, column=1, pady=pady, padx=padx, sticky=tk.W)

        # Email
        tk.Label(self.root, text='Email:', font=label_font).grid(row=3, column=0, pady=pady, padx=padx, sticky=tk.E)
        self.email_entry = tk.Entry(self.root, font=entry_font)
        self.email_entry.grid(row=3, column=1, pady=pady, padx=padx, sticky=tk.W)

        # Password
        tk.Label(self.root, text='Password:', font=label_font).grid(row=4, column=0, pady=pady, padx=padx, sticky=tk.E)
        self.pw_entry = tk.Entry(self.root, font=entry_font, show='*')
        self.pw_entry.grid(row=4, column=1, pady=pady, padx=padx, sticky=tk.W)

        # Retype Password
        tk.Label(self.root, text='Retype Password:', font=label_font).grid(row=5, column=0, pady=pady, padx=padx, sticky=tk.E)
        self.repw_entry = tk.Entry(self.root, font=entry_font, show='*')
        self.repw_entry.grid(row=5, column=1, pady=pady, padx=padx, sticky=tk.W)

        # Role
        tk.Label(self.root, text='Role (user/admin):', font=label_font).grid(row=6, column=0, pady=pady, padx=padx, sticky=tk.E)
        self.role_entry = tk.Entry(self.root, font=entry_font)
        self.role_entry.grid(row=6, column=1, pady=pady, padx=padx, sticky=tk.W)

    def save_user(self):
        name = self.name_entry.get()
        dob_str = self.dob_entry.get()
        email = self.email_entry.get()
        password = self.pw_entry.get()
        re_password = self.repw_entry.get()
        role = self.role_entry.get()

        # Validate form fields
        if not all([name, dob_str, email, password, re_password, role]):
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

        # Check if admin/user
        if role != 'user' and role != 'admin':
            mb.showerror("Error", "Role must be user/admin only.")
            return

        # Hash the password
        hashed_password = self.hash_password(password)

        # Create new user and save to file
        new_user = {
            'name': name,
            'dob': dob_str,
            'email': email,
            'password': hashed_password.decode('utf-8'),
            'role': role
        }
        self.users.append(new_user)
        self.save_users(self.users)
        mb.showinfo("Success", "User added successfully")
        self.manage_users_event()  # refresh the manage users window after adding a new user

    def edit_user_event(self):
        selected_item = self.user_tree.selection()
        if not selected_item:
            mb.showerror("Error", "Please select a user to edit.")
            return

        user_id = int(self.user_tree.item(selected_item[0], 'values')[0])
        self.editing_user = self.users[user_id]

        self.clear_window()
        tk.Label(self.root, text='EDIT USER DETAILS', font=('Arial', 24, 'bold'), fg='white', bg='#58A4B0', borderwidth=2,
                 relief='solid').grid(row=0, columnspan=2, pady=5, padx=20, sticky='n')

        # User form with existing data
        self.create_user_form()
        self.name_entry.insert(0, self.editing_user['name'])
        self.dob_entry.insert(0, self.editing_user['dob'])
        self.email_entry.insert(0, self.editing_user['email'])
        self.role_entry.insert(0, self.editing_user['role'])

        button_font = ('Arial', 13)

        # Save and Cancel buttons
        tk.Button(self.root, text='Save Changes', font= button_font, command=self.save_edited_user).grid(row=7, columnspan=2, pady=5)
        tk.Button(self.root, text='Cancel', font= button_font, command=self.manage_users_event).grid(row=8, columnspan=2, pady=5)

    def save_edited_user(self):
        name = self.name_entry.get()
        dob_str = self.dob_entry.get()
        email = self.email_entry.get()
        role = self.role_entry.get()
        pw = self.pw_entry.get()
        repw = self.repw_entry.get()

        # Validate password
        if not self.validate_password(pw, repw):
            mb.showerror("Error", "Passwords do not match.")
            return

        # Validate form fields
        if not all([name, dob_str, email, role]):
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
        hashed_password = self.hash_password(pw)

        # Update the user details
        self.editing_user.update(
            {'name': name, 'dob': dob_str, 'email': email, 'role': role, 'password': hashed_password.decode('utf-8')})

        # Save the updated users list to the file
        self.save_users(self.users)
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
            self.save_users(self.users)
            mb.showinfo("Success", "User deleted successfully")
            self.manage_users_event()


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='#BAC1B8')
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.resizable(width=True, height=True)
    app = UserAuthApp(root)
    root.mainloop()




