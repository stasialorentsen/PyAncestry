import tkinter as tk
from tkinter import messagebox
from database_operations import search_person

class PersonSearchForm:
    # Implementation of PersonSearchForm
    class PersonSearchForm:
        def __init__(self, master, driver):
            self.master = master
            master.title("Search Person")

            # Create a label and entry field for search parameter
            self.label_search = tk.Label(master, text="Search:")
            self.label_search.grid(row=0, column=0, sticky="w")
            self.entry_search = tk.Entry(master)
            self.entry_search.grid(row=0, column=1)

            # Create a listbox to display search results
            self.listbox = tk.Listbox(master)
            self.listbox.grid(row=1, columnspan=2)

            # Create the search button
            self.search_button = tk.Button(master, text="Search", command=self.person_search)
            self.search_button.grid(row=2, columnspan=2)

            self.driver = driver
            
            
    def person_search(self):
        # Retrieve the search parameter from the entry field
        search_param = self.entry_search.get()

        # Perform search operation based on the provided parameter
        if search_param:
            with self.driver.session() as session:
                results = session.write_transaction(search_person, search_param)
                self.display_search_results(results)
        else:
            messagebox.showwarning("Search Criteria", "Please enter a search parameter.")

    def display_search_results(self, results):
        # Clear previous search results
        self.listbox.delete(0, tk.END)
        
        # Display new search results
        for person in results:
            self.listbox.insert(tk.END, f"{person['name']} {person['surname']}")

        # Create the buttons for add relationship and view person
        self.add_relationship_button = tk.Button(self.master, text="Add Relationship", command=self.add_relationship)
        self.add_relationship_button.grid(row=3, column=0, pady=10)

        self.view_person_button = tk.Button(self.master, text="View Person", command=self.view_person)
        self.view_person_button.grid(row=3, column=1, pady=10)

    def view_person(self):
    # Retrieve the selected person from the listbox
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_person_name = self.listbox.get(selected_index)  # Retrieve the selected person's name
            root = tk.Tk()
            app = ViewPersonForm(root, selected_person_name, self.driver)  # Pass the name of the selected person
            app.fetch_person_details()  # Call the fetch_person_details method
            root.mainloop()
        else:
            messagebox.showwarning("No Selection", "Please select a person.")
            
    def add_relationship(self):
        print("Add relationship")
        # Retrieve the selected person from the listbox
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_person_name = self.listbox.get(selected_index)  # Retrieve the selected person's name
            root = tk.Tk()
            app = AddRelationshipForm(root, selected_person_name, self.driver)  # Pass the name of the selected person
            root.mainloop()
        else:
            messagebox.showwarning("No Selection", "Please select a person.")

class AddRelationshipForm:
    # Implementation of AddRelationshipForm
    class AddRelationshipForm:
        def __init__(self, master, selected_person, driver):
            self.master = master
            master.title("Add Relationship")

            # Store the selected person
            self.selected_person = selected_person

            # Store the Neo4j driver
            self.driver = driver

            # Create the main frame
            self.frame = tk.Frame(master)
            self.frame.pack()

            # Create labels and entry fields for the relationship details
            self.label_relationship = tk.Label(self.frame, text="Relationship Type:")
            self.label_relationship.grid(row=0, column=0, sticky="w")
            self.entry_relationship = tk.Entry(self.frame)
            self.entry_relationship.grid(row=0, column=1)

            # Create the button for selecting a person
            self.select_person_button = tk.Button(self.frame, text="Select Person", command=self.select_person)
            self.select_person_button.grid(row=1, columnspan=2)
