import tkinter as tk

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
