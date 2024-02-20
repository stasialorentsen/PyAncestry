<<<<<<< HEAD
import tkinter as tk
from tkinter import messagebox
from database_operations import search_person, view_person
from ViewDetailsForm import ViewDetailsForm


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
                self.results = session.write_transaction(search_person, search_param)
                # Displaying the search results
                self.display_search_results(self.results)
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
                
            # Create the buttons for add relationship, view person, and view details
            self.view_details_button = tk.Button(self.master, text="View Person", command=self.view_details)
            self.view_details_button.grid(row=3, column=0, pady=10)
            #self.view_details_button = tk.Button(self.master, text="Add Relationship", command=self.view_details)
            self.view_details_button.grid(row=3, column=1, pady=10)
        else:
            # Displaying an informational message if no matching persons are found
            messagebox.showinfo("No Results", "No matching persons found.")
    
    # Method to view details of the selected person
    def view_details(self):
        # Retrieve the selected person from the listbox
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_person = self.results[selected_index[0]]  # Retrieve the selected person's details from the results list
            root = tk.Tk()
            app = ViewDetailsForm(root, self.driver, selected_person['name'], selected_person['surname'], selected_person['birthdate'])
            app.fetch_details()
            root.mainloop()
        else:
            messagebox.showwarning("No Selection", "Please select a person.")

            
    # Method to add relationship to the selected person
    # def add_relationship(self):
=======
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
>>>>>>> 47882a43ed388914e5cd84941a7242a8d981e127
