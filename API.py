import tkinter as tk
from tkinter import ttk
import re
import json
import bcrypt
import os
from datetime import datetime
import tkinter.messagebox as mb
import requests



def fetch_category_data():
    url = f"http://openlibrary.org/subjects/fiction.json"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        # Process and format data immediately
        format_book_data(data)

        print("Category data fetched and saved successfully.")
    except requests.RequestException as e:
        print(f"Failed to fetch data: {e}")


def format_book_data(data):
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
        print(f"An error occurred while formatting data: {e}")

fetch_category_data()