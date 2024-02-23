import tkinter as tk

class AddRelationshipForm:
    # Constructor method to initialize the form
    def __init__(self, master, driver, selected_person_info):
        self.master = master
        self.driver = driver
        self.selected_person_info = selected_person_info
        
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
        
        # Populate selected person's information
        self.entry_selected_name.insert(tk.END, self.selected_person_info['name'])
        self.entry_selected_surname.insert(tk.END, self.selected_person_info['surname'])
        self.entry_selected_birthdate.insert(tk.END, self.selected_person_info['birthdate'])
        
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
