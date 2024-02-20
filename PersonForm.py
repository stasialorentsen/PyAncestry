import tkinter as tk
from tkinter import messagebox
from database_operations import create_person

# Class representing the form for creating a new person
class PersonForm:
    # Constructor method to initialize the form
    def __init__(self, master, driver):
        # Initializing the master (root) window and the Neo4j driver
        self.master = master
        self.driver = driver
        # Setting the title of the form
        master.title("Create Person")

        # Creating labels and entry fields for name, surname, and birthdate
        self.label_name = tk.Label(master, text="Name:")
        self.label_name.grid(row=0, column=0, sticky="w")
        self.entry_name = tk.Entry(master)
        self.entry_name.grid(row=0, column=1)

        self.label_surname = tk.Label(master, text="Surname:")
        self.label_surname.grid(row=1, column=0, sticky="w")
        self.entry_surname = tk.Entry(master)
        self.entry_surname.grid(row=1, column=1)

        self.label_birthdate = tk.Label(master, text="Birthdate:")
        self.label_birthdate.grid(row=2, column=0, sticky="w")
        self.entry_birthdate = tk.Entry(master)
        self.entry_birthdate.grid(row=2, column=1)

        # Creating the 'Create Person' button
        self.submit_button = tk.Button(master, text="Create Person", command=self.create_person)
        self.submit_button.grid(row=3, columnspan=2)

    # Method to create a new person
    def create_person(self):
        # Retrieving user input from the entry fields
        name = self.entry_name.get()
        surname = self.entry_surname.get()
        birthdate = self.entry_birthdate.get()

        # Checking if all fields are filled
        if name and surname and birthdate:
            # Creating a dictionary with person details
            person_details = {"name": name, "surname": surname, "birthdate": birthdate}
            # Calling the add_person method to add the person to the database
            self.add_person(person_details)
            # Displaying a success message
            messagebox.showinfo("Success", "Person created successfully!")
            # Clearing the form fields
            self.clear_form()
        else:
            # Displaying an error message if any field is empty
            messagebox.showerror("Error", "Please fill in all fields.")

    # Method to add a person to the database
    def add_person(self, person_details):
        # Using the provided Neo4j driver to interact with the database
        with self.driver.session() as session:
            # Calling the create_person function from database_operations module
            create_person(session, person_details)

    # Method to clear the form fields
    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_surname.delete(0, tk.END)
        self.entry_birthdate.delete(0, tk.END)
