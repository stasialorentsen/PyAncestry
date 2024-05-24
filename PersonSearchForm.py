import tkinter as tk
from tkinter import messagebox
from database_operations import search_person_by_name_or_surname, view_person_details, add_relationship_in_db, delete_person_by_id, check_relationships_by_id
from EditPersonForm import EditPersonForm


class PersonSearchForm:
    def __init__(self, master, driver):
        self.master = master
        self.driver = driver
        self.results1 = []
        self.results2 = []

        master.title("Search Person")

        # Column 1: Person 1 search
        self.label_name1 = tk.Label(master, text="Person 1 Name:")
        self.label_name1.grid(row=0, column=0, sticky="w")
        self.entry_name1 = tk.Entry(master)
        self.entry_name1.grid(row=0, column=1)

        self.label_surname1 = tk.Label(master, text="Person 1 Surname:")
        self.label_surname1.grid(row=1, column=0, sticky="w")
        self.entry_surname1 = tk.Entry(master)
        self.entry_surname1.grid(row=1, column=1)

        self.search_button1 = tk.Button(master, text="Search Person 1", command=self.person1_search)
        self.search_button1.grid(row=2, column=0, columnspan=2)

        self.listbox1 = tk.Listbox(master, exportselection=False)
        self.listbox1.grid(row=3, column=0, columnspan=2)
        self.listbox1.bind('<<ListboxSelect>>', self.on_listbox1_select)

        self.view_details_text1 = tk.Text(master, height=5, width=30)
        self.view_details_text1.grid(row=4, column=0, columnspan=2)

        # Column 2: Person 2 search
        self.label_name2 = tk.Label(master, text="Person 2 Name:")
        self.label_name2.grid(row=0, column=2, sticky="w")
        self.entry_name2 = tk.Entry(master)
        self.entry_name2.grid(row=0, column=3)

        self.label_surname2 = tk.Label(master, text="Person 2 Surname:")
        self.label_surname2.grid(row=1, column=2, sticky="w")
        self.entry_surname2 = tk.Entry(master)
        self.entry_surname2.grid(row=1, column=3)

        self.search_button2 = tk.Button(master, text="Search Person 2", command=self.person2_search)
        self.search_button2.grid(row=2, column=2, columnspan=2)

        self.listbox2 = tk.Listbox(master, exportselection=False)
        self.listbox2.grid(row=3, column=2, columnspan=2)
        self.listbox2.bind('<<ListboxSelect>>', self.on_listbox2_select)

        self.view_details_text2 = tk.Text(master, height=5, width=30)
        self.view_details_text2.grid(row=4, column=2, columnspan=2)
        
        self.edit_button1 = tk.Button(master, text="Edit Person 1", command=lambda: self.edit_person(1))
        self.edit_button1.grid(row=5, column=0, columnspan=2)
        
        self.edit_button2 = tk.Button(master, text="Edit Person 2", command=lambda: self.edit_person(2))
        self.edit_button2.grid(row=5, column=2, columnspan=2)
        
        self.delete_button1 = tk.Button(master, text="Delete Person 1", command=lambda: self.delete_person(1))
        self.delete_button1.grid(row=6, column=0, columnspan=2)
        
        self.delete_button2 = tk.Button(master, text="Delete Person 2", command=lambda: self.delete_person(2))
        self.delete_button2.grid(row=6, column=2, columnspan=2)

        # Relationship details
        self.label_relationship_type = tk.Label(master, text="Relationship Type:")
        self.label_relationship_type.grid(row=9, column=0, columnspan=2)

        self.relationship_type_var = tk.StringVar(master)
        self.relationship_type_var.set("Married to")  # Default relationship type
        self.relationship_type_dropdown = tk.OptionMenu(master, self.relationship_type_var, "Married to", "A parent of", "A child of")
        self.relationship_type_dropdown.grid(row=9, column=1, columnspan=2)

        self.add_relationship_button = tk.Button(master, text="Add Relationship", command=self.add_relationship)
        self.add_relationship_button.grid(row=9, column=2, columnspan=4)
        


    def person1_search(self):
        name = self.entry_name1.get()
        surname = self.entry_surname1.get()
        with self.driver.session() as session:
            results = session.write_transaction(search_person_by_name_or_surname, name, surname)
            self.results1 = results
            self.display_search_results(results, self.listbox1)

    def person2_search(self):
        name = self.entry_name2.get()
        surname = self.entry_surname2.get()
        with self.driver.session() as session:
            results = session.write_transaction(search_person_by_name_or_surname, name, surname)
            self.results2 = results
            self.display_search_results(results, self.listbox2)

    def display_search_results(self, results, listbox):
        listbox.delete(0, tk.END)
        for record in results:
            name = record['name']
            surname = record['surname']
            birthdate = record['birthdate']
            display_text = f"{name} {surname} {birthdate}"
            listbox.insert(tk.END, display_text)

    def on_listbox1_select(self, event):
        self.display_person_details(self.listbox1, self.results1, self.view_details_text1)

    def on_listbox2_select(self, event):
        self.display_person_details(self.listbox2, self.results2, self.view_details_text2)
    
    def display_person_details(self, listbox, results, text_widget):
        selected_index = listbox.curselection()
        if selected_index and results:  
            selected_person = results[selected_index[0]]
            name = selected_person.get('name')
            surname = selected_person.get('surname')
            birthdate = selected_person.get('birthdate')
            person_id = selected_person.get('person_id')  # Get the id of the selected person
            with self.driver.session() as session:
                person_details = session.read_transaction(view_person_details, name, surname, birthdate, person_id)  
                self.update_text_widget(text_widget, person_details)
        else:
            self.update_text_widget(text_widget, "No person selected.")

    
    def update_text_widget(self, text_widget, details):
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        if details:
            text_widget.insert(tk.END, f"Name: {details['name']}\nSurname: {details['surname']}\nBirthdate: {details['birthdate']}")
        else:
            text_widget.insert(tk.END, "No details found.")
        text_widget.config(state=tk.DISABLED)
        

    def edit_person(self, person_number):
        if person_number == 1:
            selected_index = self.listbox1.curselection()
            if selected_index:
                selected_person = self.results1[selected_index[0]]
                print("Selected Person:", selected_person)
                person_id = selected_person.get('person_id') 
                name = selected_person.get('name')
                surname = selected_person.get('surname')
                birthdate = selected_person.get('birthdate')
                
                # Open a new window for editing the person
                edit_window = tk.Toplevel(self.master)
                edit_window.title("Edit Person 1")
                
                # Instantiate the EditPersonForm for editing person details
                print("Person ID before creating EditPersonForm:", person_id)
                edit_form = EditPersonForm(edit_window, self.driver, person_id, name, surname, birthdate)
        
            else:
                messagebox.showwarning("No Selection", "Please select a person 1 to edit.")
    
        elif person_number == 2:
            selected_index = self.listbox2.curselection()
            if selected_index:
                selected_person = self.results2[selected_index[0]]
                person_id = selected_person.get('person_id')  
                name = selected_person.get('name')
                surname = selected_person.get('surname')
                birthdate = selected_person.get('birthdate')
                
                # Open a new window for editing the person
                edit_window = tk.Toplevel(self.master)
                edit_window.title("Edit Person 2")
                
                # Instantiate the EditPersonForm for editing person details
                edit_form = EditPersonForm(edit_window, self.driver, person_id, name, surname, birthdate)
        
            else:
                messagebox.showwarning("No Selection", "Please select a person 2 to edit.")
    
    # Call edit_person with argument 1 for the first button
    def edit_person1(self):
        self.edit_person(1)
    
    # Call edit_person with argument 2 for the second button
    def edit_person2(self):
        self.edit_person(2)

    def add_relationship(self):
        selected_index1 = self.listbox1.curselection()
        selected_index2 = self.listbox2.curselection()
        
        if selected_index1 and selected_index2:
            selected_person1 = self.results1[selected_index1[0]]
            selected_person2 = self.results2[selected_index2[0]]
            
            print("Selected Person 1:", selected_person1)
            print("Selected Person 2:", selected_person2)
            
            person1_id = selected_person1.get('person_id')
            person2_id = selected_person2.get('person_id')
            
            if not person1_id or not person2_id:
                messagebox.showerror("Error", "One or both selected persons do not have a valid ID.")
                return
            
            relationship_type = self.relationship_type_var.get()
            
            print(f"Person ID 1: {person1_id}, Person ID 2: {person2_id}, Relationship Type: {relationship_type}")
            
            with self.driver.session() as session:
                session.write_transaction(add_relationship_in_db, person1_id, person2_id, relationship_type)
            
            messagebox.showinfo("Success", "Relationship added successfully.")
        else:
            messagebox.showwarning("No Selection", "Please select persons 1 and 2.")

    def check_relationships(self, person_id):
        # Check if person_id is not null or empty
        if person_id:
            # Query the database to check if the person has any relationships
            with self.driver.session() as session:
                relationship_count = session.read_transaction(check_relationships_by_id, person_id)
                
                # Print the relationship count for debugging
                print("Relationship Count:", relationship_count)
            
            # Return True if relationships exist, False otherwise
            return relationship_count > 0
        else:
            # If person_id is null or empty, return False
            return False
    
    def delete_person(self, person_number):
        if person_number == 1:
            selected_index = self.listbox1.curselection()
            if selected_index:
                selected_person = self.results1[selected_index[0]]
                person_id = selected_person.get('person_id') 
                name = selected_person.get('name')
                surname = selected_person.get('surname')
                birthdate = selected_person.get('birthdate')
    
                # Check if the person has relationships
                has_relationships = self.check_relationships(person_id)
                
                # Display a confirmation dialog with appropriate message
                if has_relationships:
                    confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {name} {surname} and all their relationships?")
                else:
                    confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {name} {surname}?")
                
                if confirmation:
                    # Call the database operation method to delete the person and their relationships
                    with self.driver.session() as session:
                        session.write_transaction(delete_person_by_id, person_id)
            else:
                messagebox.showwarning("No Selection", "Please select a person 1 to delete.")
    
        elif person_number == 2:
            selected_index = self.listbox2.curselection()
            if selected_index:
                selected_person = self.results2[selected_index[0]]
                person_id = selected_person.get('person_id')  
                name = selected_person.get('name')
                surname = selected_person.get('surname')
                birthdate = selected_person.get('birthdate')
    
                # Check if the person has relationships
                has_relationships = self.check_relationships(person_id)
                
                # Display a confirmation dialog with appropriate message
                if has_relationships:
                    confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {name} {surname} and all their relationships?")
                else:
                    confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {name} {surname}?")
                
                if confirmation:
                    # Call the database operation method to delete the person and their relationships
                    with self.driver.session() as session:
                        session.write_transaction(delete_person_by_id, person_id)
            else:
                messagebox.showwarning("No Selection", "Please select a person 2 to delete.")
    
    def delete_person1(self):
        self.delete_person(1)
    
    def delete_person2(self):
        self.delete_person(2)
    
