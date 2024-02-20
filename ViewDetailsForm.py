import tkinter as tk
from tkinter import messagebox
from database_operations import view_person

class ViewDetailsForm:
    # Constructor method to initialize the form
    def __init__(self, master, driver, name, surname, birthdate):
        # Initializing the master (root) window and the Neo4j driver
        self.master = master
        self.driver = driver
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        # Setting the title of the form
        master.title("View Details")

        # Creating labels and entry fields for name, surname, and birthdate
        self.label_name = tk.Label(master, text="Name:")
        self.label_name.grid(row=0, column=0, sticky="w")
        self.entry_name = tk.Entry(master, state='readonly')  # Readonly to prevent editing
        self.entry_name.grid(row=0, column=1)

        self.label_surname = tk.Label(master, text="Surname:")
        self.label_surname.grid(row=1, column=0, sticky="w")
        self.entry_surname = tk.Entry(master, state='readonly')
        self.entry_surname.grid(row=1, column=1)

        self.label_birthdate = tk.Label(master, text="Birthdate:")
        self.label_birthdate.grid(row=2, column=0, sticky="w")
        self.entry_birthdate = tk.Entry(master, state='readonly')
        self.entry_birthdate.grid(row=2, column=1)

        # Setting the initial values of the entry fields
        self.entry_name.insert(tk.END, name)
        self.entry_surname.insert(tk.END, surname)
        self.entry_birthdate.insert(tk.END, birthdate)
