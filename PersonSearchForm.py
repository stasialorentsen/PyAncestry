import tkinter as tk
from tkinter import messagebox
from database_operations import search_person_by_name_or_surname, view_person_details
from ViewDetailsForm import ViewDetailsForm

class PersonSearchForm:
    # Constructor method to initialize the form
    def __init__(self, master, driver):
        # Initializing the master (root) window and the Neo4j driver
        self.master = master
        self.driver = driver
        self.results = [] # Initialize results attribute
        # Setting the title of the form
        master.title("Search Person")

        # Creating labels and entry fields for name and surname
        self.label_name = tk.Label(master, text="Name:")
        self.label_name.grid(row=0, column=0, sticky="w")
        self.entry_name = tk.Entry(master)
        self.entry_name.grid(row=0, column=1)

        self.label_surname = tk.Label(master, text="Surname:")
        self.label_surname.grid(row=1, column=0, sticky="w")
        self.entry_surname = tk.Entry(master)
        self.entry_surname.grid(row=1, column=1)

        # Creating a listbox to display search results
        self.listbox = tk.Listbox(master)
        self.listbox.grid(row=2, columnspan=2)

        # Creating the 'Search' button
        self.search_button = tk.Button(master, text="Search", command=self.person_search)
        self.search_button.grid(row=3, columnspan=2)
        
        # Create the View Details button
        self.view_details_button = tk.Button(master, text="View Details", command=self.view_details)
        self.view_details_button.grid(row=3, column=2)  # Placing on the next column
        
        # Create the Add Relationship button
        self.view_details_button = tk.Button(master, text="Add Relationship", command=self.add_relationship)
        self.view_details_button.grid(row=3, column=3)  # Placing on the next column


    # Method to perform the search operation
    def person_search(self):
        # Retrieving the search parameters from the entry fields
        name = self.entry_name.get()
        surname = self.entry_surname.get()
    
        # Performing the search operation using the provided parameters
        with self.driver.session() as session:
            # Calling the search_person_by_name_and_surname function from database_operations module
            results = session.write_transaction(search_person_by_name_or_surname, name, surname)
            self.results = results  # Update results attribute
    
            # Displaying the search results
            self.display_search_results(results)
    

    # Method to display the search results in the listbox
    def display_search_results(self, result):
        # Clearing the previous search results from the listbox
        self.listbox.delete(0, tk.END)

        # Displaying new search results if any
        for record in result:
            name = record['name']
            surname = record['surname']
            birthdate = record['birthdate']
            display_text = f"{name} {surname} {birthdate}"
            self.listbox.insert(tk.END, display_text)

    
    # Method to display selected person's details
    def view_details(self):
       selected_index = self.listbox.curselection()
       if selected_index:
           selected_person = self.results[selected_index[0]]
           name = selected_person.get('name')
           surname = selected_person.get('surname')
           birthdate = selected_person.get('birthdate')
           
           with self.driver.session() as session:
               person_details = session.read_transaction(view_person_details, name, surname, birthdate)
           
           if person_details:
               messagebox.showinfo("Person Details", f"Name: {person_details['name']}\nSurname: {person_details['surname']}\nBirthdate: {person_details['birthdate']}")
           else:
               messagebox.showinfo("No Details", "No details found for the selected person.")
       else:
           messagebox.showwarning("No Selection", "Please select a person.")
                 
    # Method to add relationship to the selected person
    def add_relationship(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_person = self.results[selected_index[0]]
            name = selected_person.get('name')
            surname = selected_person.get('surname')
            birthdate = selected_person.get('birthdate')
            
            with self.driver.session() as session:
                relationship_details = session.read_transaction(add_relationship, name, surname, birthdate)