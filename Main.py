# Install dependencies from requirements.txt
pip install -r requirements.txt

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
import tkinter as tk
from tkinter import messagebox

from PersonForm import PersonForm
from PersonSearchForm import PersonSearchForm

load_dotenv('.env')

uri = os.getenv('NEO4J_URI')
username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')

driver = GraphDatabase.driver(uri, auth=(username, password))

class MainForm:
    def __init__(self, master):
        self.master = master
        master.title("Person Management System")

        self.create_button = tk.Button(master, text="Create Person", command=self.open_create_person)
        self.create_button.pack(pady=10)

        self.search_button = tk.Button(master, text="Search Person", command=self.open_search_person)
        self.search_button.pack(pady=10)

    def open_create_person(self):
        # Open the Create Person form
        root = tk.Tk()
        app = PersonForm(root, driver)
        # Assign the create_person method to the submit button command
        app.submit_button.config(command=app.create_person)
        root.mainloop()

    def open_search_person(self):
        root = tk.Tk()
        app = PersonSearchForm(root, driver)
        root.mainloop()
        
def main():
    root = tk.Tk()
    app = MainForm(root)
    root.mainloop()

if __name__ == "__main__":
    main()
