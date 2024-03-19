import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database_operations import add_relationship

class AddRelationshipForm:
    # Constructor method to initialize the form
    def __init__(self, master, driver, name, surname, birthdate):
        self.master = master
        self.driver = driver
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        
        # Create frames for organizing widgets
        self.frame_selected_person = tk.Frame(master)
        self.frame_selected_person.grid(row=0, column=0, padx=10, pady=10)
        
        self.frame_new_person = tk.Frame(master)
        self.frame_new_person.grid(row=0, column=1, padx=10, pady=10)
        
        # Create labels and entry fields for selected person's information
        self.label_selected_name = tk.Label(self.frame_selected_person, text="Name:")
        self.label_selected_name.grid(row=0, column=0, sticky="w")
        self.entry_selected_name = tk.Entry(self.frame_selected_person, state='readonly')
        self.entry_selected_name.grid(row=0, column=1)

        self.label_selected_surname = tk.Label(self.frame_selected_person, text="Surname:")
        self.label_selected_surname.grid(row=1, column=0, sticky="w")
        self.entry_selected_surname = tk.Entry(self.frame_selected_person, state='readonly')
        self.entry_selected_surname.grid(row=1, column=1)

        self.label_selected_birthdate = tk.Label(self.frame_selected_person, text="Birthdate:")
        self.label_selected_birthdate.grid(row=2, column=0, sticky="w")
        self.entry_selected_birthdate = tk.Entry(self.frame_selected_person, state='readonly')
        self.entry_selected_birthdate.grid(row=2, column=1)
        
        # # Populate selected person's information - TO-DO better
        self.entry_selected_name.configure(state='normal')  # Change state to normal temporarily
        self.entry_selected_name.delete(0, tk.END)  # Clear any existing text
        self.entry_selected_name.insert(tk.END, self.name)  # Insert the new value
        self.entry_selected_name.configure(state='readonly')  # Change state back to readonly
        
        self.entry_selected_surname.configure(state='normal')
        self.entry_selected_surname.delete(0, tk.END)
        self.entry_selected_surname.insert(tk.END, self.surname)
        self.entry_selected_surname.configure(state='readonly')
        
        self.entry_selected_birthdate.configure(state='normal')
        self.entry_selected_birthdate.delete(0, tk.END)
        self.entry_selected_birthdate.insert(tk.END, self.birthdate)
        self.entry_selected_birthdate.configure(state='readonly')

        
        # Create labels and entry fields for new person's information
        self.label_new_name = tk.Label(self.frame_new_person, text="Name 2:")
        self.label_new_name.grid(row=0, column=0, sticky="w")
        self.entry_new_name = tk.Entry(self.frame_new_person)
        self.entry_new_name.grid(row=0, column=1)

        self.label_new_surname = tk.Label(self.frame_new_person, text="Surname 2:")
        self.label_new_surname.grid(row=1, column=0, sticky="w")
        self.entry_new_surname = tk.Entry(self.frame_new_person)
        self.entry_new_surname.grid(row=1, column=1)

        self.label_new_birthdate = tk.Label(self.frame_new_person, text="Birthdate 2:")
        self.label_new_birthdate.grid(row=2, column=0, sticky="w")
        self.entry_new_birthdate = tk.Entry(self.frame_new_person)
        self.entry_new_birthdate.grid(row=2, column=1)
        
        # Create dropdown for relationship type
        self.label_relationship_type = tk.Label(master, text="Relationship Type:")
        self.label_relationship_type.grid(row=3, column=0)
        self.relationship_type_var = tk.StringVar(master)
        self.relationship_type_var.set("Married to")  # Default relationship type
        self.relationship_type_dropdown = ttk.Combobox(master, textvariable=self.relationship_type_var, values=["Married to", "A parent of", "A child of"])
        self.relationship_type_dropdown.grid(row=3, column=1)

        # Create the Save Relationship button
        self.save_relationship_button = tk.Button(master, text="Save Relationship", command=self.save_relationship)
        self.save_relationship_button.grid(row=3, column=2)  # Placing on the next column


    def save_relationship(self):
        person1_name = self.name
        person1_surname = self.surname
        person1_birthdate = self.birthdate
        person2_name = self.entry_new_name.get()
        person2_surname = self.entry_new_surname.get()
        person2_birthdate = self.entry_new_birthdate.get()
        
        # Check if person2_name is empty
        if not person2_name:
            messagebox.showerror("Error", "Please fill in at least the name for the second person.")
            return  # Exit the method without attempting to save the relationship
        
        # Retrieve the selected relationship type
        relationship_type = self.relationship_type_var.get()
        
        # Call the add_relationship function from database_operations module with the provided details
        with self.driver.session() as session:
            result = session.write_transaction(add_relationship, person1_name, person1_surname, person1_birthdate, person2_name, person2_surname, person2_birthdate, relationship_type)
        
        # Print the result
        # print("Transaction Result:", result)
        
        if result is not None:
            messagebox.showinfo("Success", "Relationship added successfully.")
        else:
            messagebox.showerror("Error", "Failed to add relationship.")


               
