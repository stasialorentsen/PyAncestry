import tkinter as tk
from tkinter import messagebox
from database_operations import search_person

# Class representing the form for searching existing persons
class PersonSearchForm:
    # Constructor method to initialize the form
    def __init__(self, master, driver):
        # Initializing the master (root) window and the Neo4j driver
        self.master = master
        self.driver = driver
        # Setting the title of the form
        master.title("Search Person")

        # Creating a label and an entry field for the search parameter
        self.label_search = tk.Label(master, text="Search:")
        self.label_search.grid(row=0, column=0, sticky="w")
        self.entry_search = tk.Entry(master)
        self.entry_search.grid(row=0, column=1)

        # Creating a listbox to display search results
        self.listbox = tk.Listbox(master)
        self.listbox.grid(row=1, columnspan=2)

        # Creating the 'Search' button
        self.search_button = tk.Button(master, text="Search", command=self.person_search)
        self.search_button.grid(row=2, columnspan=2)

    # Method to perform the search operation
    def person_search(self):
        # Retrieving the search parameter from the entry field
        search_param = self.entry_search.get()

        # Performing the search operation if the search parameter is provided
        if search_param:
            # Using the provided Neo4j driver to interact with the database
            with self.driver.session() as session:
                # Calling the search_person function from database_operations module
                results = session.write_transaction(search_person, search_param)
                # Displaying the search results
                self.display_search_results(results)
        else:
            # Displaying a warning message if no search parameter is provided
            messagebox.showwarning("Search Criteria", "Please enter a search parameter.")

    # Method to display the search results in the listbox
    def display_search_results(self, results):
        # Clearing the previous search results from the listbox
        self.listbox.delete(0, tk.END)

        # Displaying new search results if any
        if results:
            # Iterating through the search results and adding them to the listbox
            for person in results:
                name = person.get('name', '')
                surname = person.get('surname', '')
                birthdate = person.get('birthdate', '')
                display_text = f"{name} {surname} {birthdate}"
                self.listbox.insert(tk.END, display_text)
        else:
            # Displaying an informational message if no matching persons are found
            messagebox.showinfo("No Results", "No matching persons found.")
